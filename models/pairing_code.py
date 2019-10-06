from marshmallow import fields, validate, Schema


# pairing code is stored in instrument table and does not need a separate model


class PairingCodeSchema(Schema):
    instrument_name = fields.String(validate=validate.Length(min=1, max=250), required=True)
    pairing_code = fields.String(validate=validate.Length(min=1, max=250), required=True)


