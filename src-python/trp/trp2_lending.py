from dataclasses import dataclass, field
from typing import List
from uuid import uuid4, UUID

from trp.trp2 import TGeometry, TDocumentMetadata, TDocumentMetadataSchema, BaseSchema, TGeometrySchema, TWarnings, TWarningsSchema, TResponseMetadata, TResponseMetadataSchema
from trp.trp2_expense import TAnalyzeExpenseDocument, TExpenseSchema
from trp.trp2_analyzeid import TAnalyzeIdDocument, TIdentityDocumentSchema
import marshmallow as m


@dataclass(eq=True, init=True, repr=True)
class TLendingDetection():
    confidence: float
    geometry: TGeometry = field(default=None)
    selection_status: str = field(default=None)    #type: ignore
    text: str = field(default=None)    #type: ignore


@dataclass(eq=True, init=True, repr=True)
class TSignatureDetection():
    confidence: float
    geometry: TGeometry = field(default=None)


@dataclass(eq=True, init=True, repr=True)
class TLendingField():
    field_type: str
    value_detections: List[TLendingDetection]
    key_detection: str = field(default="")


@dataclass(eq=True, init=True, repr=True)
class TLendingDocument():
    lending_fields: List[TLendingField]
    signature_detections: List[TSignatureDetection]


@dataclass(eq=True, init=True, repr=True)
class TExtraction():
    expense_document: TAnalyzeExpenseDocument = field(default=None)
    identity_document: TAnalyzeIdDocument = field(default=None)
    lending_document: TLendingDocument = field(default=None)


@dataclass(eq=True, init=True, repr=True)
class TPrediction():
    confidence: float
    value: str


@dataclass(eq=True, init=True, repr=True)
class TPageClassification():
    page_number: List[TPrediction]
    page_type: List[TPrediction]


@dataclass(eq=True, init=True, repr=True)
class TLendingResult():
    extractions: List[TExtraction]
    page: int
    page_classification: TPageClassification


@dataclass(eq=True, init=True, repr=True)
class TFullLendingDocument():
    analyze_lending_model_version: str
    lending_results: List[TLendingResult]
    document_metadata: TDocumentMetadata
    job_status: str = field(default=None)    #type: ignore
    status_message: str = field(default=None)    #type: ignore
    warnings: TWarnings = field(default=None)    #type: ignore
    response_metadata: TResponseMetadata = field(default=None)    #type: ignore
    next_token: str = field(default=None)    #type: ignore
    id: UUID = field(default_factory=uuid4)


################
# SCHEMA
###############


class TLendingDetectionSchema(BaseSchema):
    confidence = m.fields.Float(data_key="Confidence")
    geometry = m.fields.Nested(TGeometrySchema, data_key="Geometry", required=False)
    selection_status = m.fields.String(data_key="SelectionStatus")
    text = m.fields.String(data_key="Text")

    @m.post_load
    def make(self, data, **kwargs):
        return TLendingDetection(**data)


class TSignatureDetectionSchema(BaseSchema):
    confidence = m.fields.Float(data_key="Confidence")
    geometry = m.fields.Nested(TGeometrySchema, data_key="Geometry", required=False)

    @m.post_load
    def make(self, data, **kwargs):
        return TSignatureDetection(**data)


class TLendingFieldSchema(BaseSchema):
    key_detection = m.fields.Nested(TLendingDetectionSchema, data_key="KeyDetection", required=False)
    field_type = m.fields.String(data_key="Type", required=False)
    value_detections = m.fields.List(m.fields.Nested(TLendingDetectionSchema),
                                     data_key="ValueDetections",
                                     required=False)

    @m.post_load
    def make(self, data, **kwargs):
        return TLendingField(**data)


class TLendingDocumentSchema(BaseSchema):
    lending_fields = m.fields.List(m.fields.Nested(TLendingFieldSchema), data_key="LendingFields", required=False)
    signature_detections = m.fields.List(m.fields.Nested(TSignatureDetectionSchema),
                                         data_key="SignatureDetections",
                                         required=False)

    @m.post_load
    def make(self, data, **kwargs):
        return TLendingDocument(**data)


class TExtractionSchema(BaseSchema):
    expense_document = m.fields.Nested(TExpenseSchema, data_key="ExpenseDocument", required=False, allow_none=True)
    identity_document = m.fields.Nested(TIdentityDocumentSchema,
                                        data_key="IdentityDocument",
                                        required=False,
                                        allow_none=True)
    lending_document = m.fields.Nested(TLendingDocumentSchema,
                                       data_key="LendingDocument",
                                       required=False,
                                       allow_none=True)

    @m.post_load
    def make(self, data, **kwargs):
        return TExtraction(**data)


class TPredictionSchema(BaseSchema):
    confidence = m.fields.Float(data_key="Confidence")
    value = m.fields.String(data_key="Value")

    @m.post_load
    def make(self, data, **kwargs):
        return TPrediction(**data)


class TPageClassificationSchema(BaseSchema):
    page_number = m.fields.List(m.fields.Nested(TPredictionSchema), data_key="PageNumber", required=False)
    page_type = m.fields.List(m.fields.Nested(TPredictionSchema), data_key="PageType", required=False)

    @m.post_load
    def make(self, data, **kwargs):
        return TPageClassification(**data)


class TLendingResultSchema(BaseSchema):
    extractions = m.fields.List(m.fields.Nested(TExtractionSchema),
                                data_key="Extractions",
                                required=False,
                                allow_none=True)
    page = m.fields.Int(data_key="Page", required=False)
    page_classification = m.fields.Nested(TPageClassificationSchema, data_key="PageClassification")

    @m.post_load
    def make(self, data, **kwargs):
        return TLendingResult(**data)


class TFullLendingDocumentSchema(BaseSchema):
    document_metadata = m.fields.Nested(TDocumentMetadataSchema,
                                        data_key="DocumentMetadata",
                                        required=False,
                                        allow_none=False)
    analyze_lending_model_version = m.fields.String(data_key="AnalyzeLendingModelVersion",
                                                    required=False,
                                                    allow_none=False)
    status_message = m.fields.String(data_key="StatusMessage", required=False, allow_none=True)
    warnings = m.fields.Nested(TWarningsSchema, data_key="Warnings", required=False, allow_none=True)
    job_status = m.fields.String(data_key="JobStatus", required=False, allow_none=True)
    next_token = m.fields.String(data_key="NextToken", required=False, allow_none=True)
    response_metadata = m.fields.Nested(TResponseMetadataSchema,
                                        data_key="ResponseMetadata",
                                        required=False,
                                        allow_none=True)
    lending_results = m.fields.List(m.fields.Nested(TLendingResultSchema),
                                    data_key="Results",
                                    required=False,
                                    allow_none=True)
    custom = m.fields.Dict(data_key="Custom", required=False, allow_none=True)

    @m.post_load
    def make(self, data, **kwargs):
        return TFullLendingDocument(**data)