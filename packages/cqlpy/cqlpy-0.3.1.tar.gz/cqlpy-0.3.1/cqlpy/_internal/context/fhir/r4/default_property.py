from cqlpy._internal.exceptions import CqlPyKeyError, CqlPyUnsupportedError


_DEFAULT_PROPERTIES: dict[str, str] = {
    "Account": "type",
    "ActivityDefinition": "topic",
    "AdverseEvent": "event",
    "AllergyIntolerance": "code",
    "Appointment": "serviceType",
    "Basic": "code",
    "BodyStructure": "location",
    "CarePlan": "category",
    "CareTeam": "category",
    "ChargeItem": "code",
    "ChargeItemDefinition": "code",
    "Claim": "type",
    "ClinicalImpression": "code",
    "Coding": "code",
    "Communication": "reasonCode",
    "CommunicationRequest": "category",
    "Composition": "type",
    "Condition": "code",
    "Consent": "category",
    "Coverage": "type",
    "DetectedIssue": "code",
    "Device": "type",
    "DeviceMetric": "type",
    "DeviceRequest": "code",
    "DeviceUseStatement": "device.code",
    "DiagnosticReport": "code",
    "Encounter": "type",
    "EpisodeOfCare": "type",
    "ExplanationOfBenefit": "type",
    "Flag": "code",
    "Goal": "category",
    "Group": "code",
    "GuidanceResponse": "module",
    "HealthcareService": "type",
    "Immunization": "vaccineCode",
    "Library": "topic",
    "List": "code",
    "Location": "type",
    "Measure": "topic",
    "MeasureReport": "type",
    "Medication": "code",
    "MedicationAdministration": "medication",
    "MedicationDispense": "medication",
    "MedicationKnowledge": "code",
    "MedicationRequest": "medication",
    "MedicationStatement": "medication",
    "MessageDefinition": "event",
    "Observation": "code",
    "ObservationDefinition": "code",
    "OperationDefinition": "code",
    "OperationOutcome": "issue.code",
    "PractitionerRole": "code",
    "Procedure": "code",
    "Quantity": "code",
    "Questionnaire": "name",
    "RelatedPerson": "relationship",
    "RequestGroup": "code",
    "RiskAssessment": "code",
    "SearchParameter": "target",
    "ServiceRequest": "code",
    "Specimen": "type",
    "Substance": "code",
    "SupplyDelivery": "type",
    "SupplyRequest": "category",
    "Task": "code",
    "Timing": "code",
    "UsageContext": "code",
}


def default_property(resource_type: str) -> str:
    default_property = _DEFAULT_PROPERTIES.get(resource_type, None)
    if default_property is None:
        raise CqlPyKeyError(
            f"Default property not found for resource type: {resource_type}"
        )
    if "." in default_property:
        raise CqlPyUnsupportedError(
            f"Default property is not a top-level property and is unsupported: {default_property}"
        )

    return default_property
