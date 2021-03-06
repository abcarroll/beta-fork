from marshmallow import Schema, fields, post_load

from ..meta import TypeMeta, v1_ObjectMetaSchema, v1_TypeMetaSchema
from ..registry import registry as _registry


class v1alpha1_ToolConfigAzureAuthSchema(Schema):
    client = fields.UUID()
    secret = fields.Str()


class v1alpha1_ToolConfigAzureCloudpartnerSchema(Schema):
    publisher = fields.Str()
    tenant = fields.UUID()


class v1alpha1_ToolConfigAzureImageSchema(Schema):
    group = fields.Str()
    subscription = fields.UUID()
    tenant = fields.UUID()


class v1alpha1_ToolConfigAzureStorageSchema(Schema):
    group = fields.Str()
    name = fields.Str()
    subscription = fields.UUID()
    tenant = fields.UUID()


class v1alpha1_ToolConfigAzureSchema(Schema):
    auth = fields.Nested(v1alpha1_ToolConfigAzureAuthSchema)
    cloudpartner = fields.Nested(v1alpha1_ToolConfigAzureCloudpartnerSchema)
    image = fields.Nested(v1alpha1_ToolConfigAzureImageSchema)
    storage = fields.Nested(v1alpha1_ToolConfigAzureStorageSchema)


class v1alpha1_ToolConfigEc2ImageSchema(Schema):
    regions = fields.List(fields.Str())
    tags = fields.List(fields.Str())


class v1alpha1_ToolConfigEc2Schema(Schema):
    bucket = fields.Str()
    image = fields.Nested(v1alpha1_ToolConfigEc2ImageSchema)


class v1alpha1_ToolConfigGceSchema(Schema):
    bucket = fields.Str()
    credentials_file = fields.Str(data_key='credentialsFile')
    project = fields.Str()


@_registry.register
class v1alpha1_ToolConfigSchema(v1_TypeMetaSchema):
    __typemeta__ = TypeMeta('ToolConfig', 'cloud.debian.org/v1alpha1')

    metadata = fields.Nested(v1_ObjectMetaSchema)
    azure = fields.Nested(v1alpha1_ToolConfigAzureSchema)
    ec2 = fields.Nested(v1alpha1_ToolConfigEc2Schema)
    gce = fields.Nested(v1alpha1_ToolConfigGceSchema)

    @post_load
    def load_obj(self, data, **kw):
        data.pop('api_version', None)
        data.pop('kind', None)
        return data
