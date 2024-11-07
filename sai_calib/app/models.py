from django.db import models


# Customer model
class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    primary_contact_person = models.CharField(max_length=255)
    secondary_contact_person = models.CharField(max_length=255)
    primary_email = models.EmailField()
    secondary_email = models.EmailField()
    primary_phone_no = models.CharField(max_length=15)
    secondary_phone_no = models.CharField(max_length=15)
    gst_no = models.CharField(max_length=15)
    primary_dept = models.CharField(max_length=255)
    secondary_dept = models.CharField(max_length=255)
    address = models.TextField()

# Setting Plug Trace model
class SettingPlugTrace(models.Model):
    master_name = models.CharField(max_length=255)
    id_no = models.CharField(max_length=50)
    calibration_report_no = models.CharField(max_length=50)
    valid_upto = models.CharField(max_length=50)
    traceability = models.TextField()

# Setting Ring Trace model
class SettingRingTrace(models.Model):
    master_name = models.CharField(max_length=255)
    id_no = models.CharField(max_length=50)
    calibration_report_no = models.CharField(max_length=50)
    valid_upto = models.CharField(max_length=50)
    traceability = models.TextField()

# Setting Plug Master model
class SettingPlugMaster(models.Model):
    parameter_name = models.CharField(max_length=255)
    ref_size = models.CharField(max_length=50)
    nominal = models.CharField(max_length=50)

# Setting Ring Master model
class SettingRingMaster(models.Model):
    parameter_name = models.CharField(max_length=255)
    ref_size = models.CharField(max_length=50)
    nominal = models.CharField(max_length=50)

# Engineer Manager Details model
class EngineerManagerDetails(models.Model):
    calib_engineer = models.CharField(max_length=255)
    quality_manager = models.CharField(max_length=255)
    certificate_no = models.CharField(max_length=50)

class WorkOrder(models.Model):
    customer_name = models.CharField(max_length=255)
    wo_date = models.CharField(max_length=50)  # Work Order Date
    work_order_no = models.CharField(max_length=50)
    customer_po_no = models.CharField(max_length=50, blank=True, null=True)
    customer_ref_date = models.CharField(max_length=50,blank=True, null=True)
    order_type = models.CharField(max_length=100, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    inward_no = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    hsn = models.CharField(max_length=100, blank=True, null=True)
    sr_no = models.CharField(max_length=100, blank=True, null=True)  # Serial number
    id_no = models.CharField(max_length=100, blank=True, null=True)  # ID number
    range = models.CharField(max_length=100, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    channels = models.CharField(max_length=255)
    
