from wtforms import Form, IntegerField, StringField, validators

class StructureForm(Form):
    strid = StringField('strid', validators=[validators.DataRequired("Please enter Structure id.")])
    strname = StringField('strname', validators=[validators.DataRequired("Please enter Structure name.")])
    parentid = IntegerField('parentid', validators=[validators.DataRequired("Please enter parent id.")])
    parentname = StringField('parentname', validators=[validators.DataRequired("Please enter parent name.")])


class ResourceForm(Form):
    parentid = IntegerField('Parent ID', validators=[validators.DataRequired("Please enter Parent id.")])
    parentname = StringField('Parent Name', validators=[validators.DataRequired("Please enter Parent name.")])
    resourceid = IntegerField('Resource ID', validators=[validators.DataRequired("Please enter Resource id.")])
    resourcename = StringField('Resource Name', validators=[validators.DataRequired("Please enter Resource Name.")])
    resourceamount = IntegerField('Resource Amount', validators=[validators.DataRequired("Please enter Resource Amount.")])


class DriverDataForm(Form):
    parentid = IntegerField('parentid', validators=[validators.DataRequired("Please enter Parent ID.")])
    parentname = StringField('parentname', validators=[validators.DataRequired("Please enter Parent Name.")])
    resourceid = IntegerField('resourceid', validators=[validators.DataRequired("Please enter Resource ID.")])
    resourcename = StringField('resourcename', validators=[validators.DataRequired("Please enter Resource Name.")])
    resourceamount = IntegerField('resourceamount', validators=[validators.DataRequired("Please enter Resource Amount.")])
    driverid = IntegerField('driverid', validators=[validators.DataRequired("Please enter Driver ID.")])  # Added this line

class DestinationValueForm(Form):
    driverid = StringField('driverid', validators=[validators.DataRequired("Please enter Driver ID.")])
    resourceid = IntegerField('resourceid', validators=[validators.DataRequired("Please enter Resource ID.")])
    destinationaccount = StringField('destinationaccount', validators=[validators.DataRequired("Please enter Destination Account.")])
    driverqtyunit = IntegerField('driverqtyunit', validators=[validators.DataRequired("Please enter Driver Quantity Unit.")])
