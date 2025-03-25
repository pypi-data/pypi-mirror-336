#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
#

from datetime import datetime, timezone
import uuid
from .version import VERSION


def decode_spdx(f):
    from spdx_python_model import v3_0_1 as spdx_3_0_1

    objset = spdx_3_0_1.SHACLObjectSet()

    d = spdx_3_0_1.JSONLDDeserializer()
    d.read(f, objset)
    return objset, spdx_3_0_1


def map_justification(model, j):
    if j == model.security_VexJustificationType.componentNotPresent:
        return "component_not_present"

    if j == model.security_VexJustificationType.inlineMitigationsAlreadyExist:
        return "inline_mitigations_already_exist"
    if (
        j
        == model.security_VexJustificationType.vulnerableCodeCannotBeControlledByAdversary
    ):
        return "vulnerable_code_cannot_be_controlled_by_adversary"

    if j == model.security_VexJustificationType.vulnerableCodeNotInExecutePath:
        return "vulnerable_code_not_in_execute_path"

    if j == model.security_VexJustificationType.vulnerableCodeNotPresent:
        return "vulnerable_code_not_present"

    return None


def convert_spdx_to_openvex(f, author):
    objset, model = decode_spdx(f)
    data = {
        "@context": "https://openvex.dev/ns/v0.2.0",
        "@id": "https://openvex.dev/docs/spdx3toopenvex-" + str(uuid.uuid4()),
        "author": author,
        "role": "Document Creator",
        "tooling": "spdx3toopenvex Version " + VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": 1,
        "statements": [],
    }

    cves = {}
    fixed_map = {}
    not_affected_map = {}
    affected_map = {}
    under_investigation_map = {}
    affected_packages = set()
    product_map = {}

    for v in objset.foreach_type(model.security_Vulnerability):
        for e in v.externalIdentifier:
            if e.externalIdentifierType == model.ExternalIdentifierType.cve:
                cve = e.identifier
                break
        else:
            continue

        cves[cve] = v

    def create_assessment_map(r, m):
        nonlocal affected_packages
        for v in cves.values():
            if r.from_ is v:
                m.setdefault(v, []).append(r)
                for p in r.to:
                    affected_packages.add(p)

    for r in objset.foreach_type(model.security_VexFixedVulnAssessmentRelationship):
        create_assessment_map(r, fixed_map)

    for r in objset.foreach_type(
        model.security_VexNotAffectedVulnAssessmentRelationship
    ):
        create_assessment_map(r, not_affected_map)

    for r in objset.foreach_type(model.security_VexAffectedVulnAssessmentRelationship):
        create_assessment_map(r, affected_map)

    for r in objset.foreach_type(
        model.security_VexUnderInvestigationVulnAssessmentRelationship
    ):
        create_assessment_map(r, under_investigation_map)

    for p in affected_packages:
        p_data = {
            "@id": p._id,
        }
        for e in p.externalIdentifier:
            if e.externalIdentifierType == model.ExternalIdentifierType.cpe22:
                p_data.setdefault("identifiers", {})["cpe22"] = e.identifier
            if e.externalIdentifierType == model.ExternalIdentifierType.cpe23:
                p_data.setdefault("identifiers", {})["cpe23"] = e.identifier
            if e.externalIdentifierType == model.ExternalIdentifierType.packageUrl:
                p_data.setdefault("identifiers", {})["purl"] = e.identifier

        for v in p.verifiedUsing:
            if not isinstance(v, model.Hash):
                continue

            if v.algorithm == model.HashAlgorithm.md5:
                p_data.setdefault("hashes", {})["md5"] = v.hashValue
            if v.algorithm == model.HashAlgorithm.sha1:
                p_data.setdefault("hashes", {})["sha1"] = v.hashValue
            if v.algorithm == model.HashAlgorithm.sha256:
                p_data.setdefault("hashes", {})["sha-256"] = v.hashValue
            if v.algorithm == model.HashAlgorithm.sha512:
                p_data.setdefault("hashes", {})["sha-512"] = v.hashValue

        product_map[p._id] = p_data

    def collect_products(r, statement):
        for p in r.to:
            statement["products"].add(p._id)

    def create_statement(r, cve, vuln, status):
        statement = {
            "vulnerability": {
                "@id": vuln._id,
                "name": cve,
            },
            "products": set(),
            "status": status,
        }
        if vuln.description:
            statement["vulnerability"]["description"] = vuln.description

        if r.security_statusNotes:
            statement["status_notes"] = r.security_statusNotes

        collect_products(r, statement)
        return statement

    def statement_matches(a, b):
        ignore_keys = {"products", "vulnerability"}

        for k, v in a.items():
            if k in ignore_keys:
                continue

            if k not in b:
                return False

            if b[k] != v:
                return False

        for k, v in b.items():
            if k in ignore_keys:
                continue

            if k not in a:
                return False

            if a[k] != v:
                return False

        return True

    statements_by_cve = {}

    def add_statement(cve, statement):
        nonlocal data
        nonlocal statements_by_cve
        if not statement["products"]:
            return

        for s in statements_by_cve.get(cve, []):
            if statement_matches(statement, s):
                for p in statement["products"]:
                    s["products"].add(p)

                return

        statements_by_cve.setdefault(cve, []).append(statement)
        data["statements"].append(statement)

    for cve, vuln in cves.items():
        for status, m in (
            ("fixed", fixed_map),
            ("under_investigation", under_investigation_map),
        ):
            for r in m.get(vuln, []):
                statement = create_statement(r, cve, vuln, status)
                add_statement(cve, statement)

        for r in affected_map.get(vuln, []):
            statement = create_statement(r, cve, vuln, "affected")
            if r.security_actionStatement:
                statement["action_statement"] = r.security_actionStatement

            if r.security_actionStatementTime:
                s = r.security_actionStatementTime.isoformat()
                statement["action_statement_time"] = s

            add_statement(cve, statement)

        for r in not_affected_map.get(vuln, []):
            statement = create_statement(r, cve, vuln, "not_affected")

            if r.security_justificationType:
                j = map_justification(model, r.security_justificationType)
                if j:
                    statement["justification"] = j

            if r.security_impactStatement:
                statement["impact_statement"] = r.security_impactStatement

            collect_products(r, statement)

            add_statement(cve, statement)

    for s in data["statements"]:
        s["products"] = [product_map[p] for p in sorted(s["products"])]
    data["statements"].sort(key=lambda s: s["vulnerability"]["@id"])

    return data
