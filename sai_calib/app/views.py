import json
import re
from django.http import JsonResponse
from django.shortcuts import render


from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only if CSRF tokens are difficult to implement; remove if you want CSRF protection.
def login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')

        # Check if credentials are correct
        if userid == 'admin' and password == 'admin':
            return JsonResponse({'redirect': '/index/'})  # Redirect URL to index page
        else:
            return JsonResponse({'error': 'Authentication is wrong. Please try again.'})

    return render(request, "app/login.html")


def index(request):
    return render(request,"app/index.html")


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Customer, EngineerManagerDetails, SettingPlugMaster, SettingPlugTrace, SettingRingMaster, SettingRingTrace


@csrf_exempt
def master(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            form_type = data.get('formType')
            form_data = data.get('formData')

            print("form_type",form_type)
            print("form_data",form_data)
            
            if form_type == 'customer':
                # Check if a customer with the given name already exists
                customer, created = Customer.objects.update_or_create(
                    customer_name=form_data['customer_name'],  # Use a unique field to identify the customer
                    defaults={
                        'primary_contact_person': form_data['primary_contact_person'],
                        'secondary_contact_person': form_data['secondary_contact_person'],
                        'primary_email': form_data['primary_email'],
                        'secondary_email': form_data['secondary_email'],
                        'primary_phone_no': form_data['primary_phone_no'],
                        'secondary_phone_no': form_data['secondary_phone_no'],
                        'gst_no': form_data['gst_no'],
                        'primary_dept': form_data['primary_dept'],
                        'secondary_dept': form_data['secondary_dept'],
                        'address': form_data['address']
                    }
                )

                if created:
                    message = 'New customer created successfully.'
                else:
                    message = 'Customer updated successfully.'

            elif form_type == 'setting_plug_trace':
                # Save or update setting_plug_trace table data
                for row in form_data['rows']:
                    row_id = row.get('id')  # Assuming each row has a unique ID
                    if row_id:
                        # Update existing record
                        obj = SettingPlugTrace.objects.get(id=row_id)
                        obj.master_name = row['masterName']
                        obj.id_no = row['idNo']
                        obj.calibration_report_no = row['calibrationReportNo']
                        obj.valid_upto = row['validUpto']
                        obj.traceability = row['traceability']
                        obj.save()
                    else:
                        # Create new record
                        SettingPlugTrace.objects.create(
                            master_name=row['masterName'],
                            id_no=row['idNo'],
                            calibration_report_no=row['calibrationReportNo'],
                            valid_upto=row['validUpto'],
                            traceability=row['traceability']
                        )

            elif form_type == 'setting_ring_trace':
                # Save or update setting_ring_trace table data
                for row in form_data['rows']:
                    row_id = row.get('id')  # Assuming each row has a unique ID
                    if row_id:
                        obj = SettingRingTrace.objects.get(id=row_id)
                        obj.master_name = row['masterName']
                        obj.id_no = row['idNo']
                        obj.calibration_report_no = row['calibrationReportNo']
                        obj.valid_upto = row['validUpto']
                        obj.traceability = row['traceability']
                        obj.save()
                    else:
                        SettingRingTrace.objects.create(
                            master_name=row['masterName'],
                            id_no=row['idNo'],
                            calibration_report_no=row['calibrationReportNo'],
                            valid_upto=row['validUpto'],
                            traceability=row['traceability']
                        )

            elif form_type == 'setting_plug_master':
                # Save or update setting_plug_master table data
                for row in form_data['rows']:
                    row_id = row.get('id')  # Assuming each row has a unique ID
                    if row_id:
                        obj = SettingPlugMaster.objects.get(id=row_id)
                        obj.parameter_name = row['parameterName']
                        obj.ref_size = row['refSize']
                        obj.nominal = row['nominal']
                        obj.save()
                    else:
                        SettingPlugMaster.objects.create(
                            parameter_name=row['parameterName'],
                            ref_size=row['refSize'],
                            nominal=row['nominal']
                        )

            elif form_type == 'setting_ring_master':
                # Save or update setting_ring_master table data
                for row in form_data['rows']:
                    row_id = row.get('id')  # Assuming each row has a unique ID
                    if row_id:
                        obj = SettingRingMaster.objects.get(id=row_id)
                        obj.parameter_name = row['parameterName']
                        obj.ref_size = row['refSize']
                        obj.nominal = row['nominal']
                        obj.save()
                    else:
                        SettingRingMaster.objects.create(
                            parameter_name=row['parameterName'],
                            ref_size=row['refSize'],
                            nominal=row['nominal']
                        )

            elif form_type == 'engineer_manager_details':
                # Save or update engineer_manager_details table data
                for row in form_data['rows']:
                    row_id = row.get('id')  # Assuming each row has a unique ID
                    if row_id:
                        obj = EngineerManagerDetails.objects.get(id=row_id)
                        obj.calib_engineer = row['calibEngineer']
                        obj.quality_manager = row['qualityManager']
                        obj.certificate_no = row['certificateNo']
                        obj.save()
                    else:
                        EngineerManagerDetails.objects.create(
                            calib_engineer=row['calibEngineer'],
                            quality_manager=row['qualityManager'],
                            certificate_no=row['certificateNo']
                        )

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    elif request.method == 'GET':
        customer_value = Customer.objects.all()
        SettingPlugTrace_value = SettingPlugTrace.objects.all()
        SettingRingTrace_value = SettingRingTrace.objects.all()
        SettingPlugMaster_value = SettingPlugMaster.objects.all()
        SettingRingMaster_value = SettingRingMaster.objects.all()
        EngineerManagerDetails_value = EngineerManagerDetails.objects.all()

        context ={
            'customer_value': customer_value, 
            'SettingPlugTrace_value': SettingPlugTrace_value,
            'SettingRingTrace_value': SettingRingTrace_value,
            'SettingPlugMaster_value' : SettingPlugMaster_value,
            'SettingRingMaster_value' : SettingRingMaster_value,
            'EngineerManagerDetails_value' : EngineerManagerDetails_value
        }

    elif request.method == 'DELETE':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            form_type = data.get('formType')
            ids_to_delete = data.get('idsToDelete', [])

            if form_type == 'tableBody-1':
                # Delete setting_plug_trace records
                SettingPlugTrace.objects.filter(id__in=ids_to_delete).delete()

            elif form_type == 'tableBody-2':
                # Delete setting_ring_trace records
                SettingRingTrace.objects.filter(id__in=ids_to_delete).delete()

            elif form_type == 'tableBody-3':
                # Delete setting_plug_master records
                SettingPlugMaster.objects.filter(id__in=ids_to_delete).delete()

            elif form_type == 'tableBody-4':
                # Delete setting_ring_master records
                SettingRingMaster.objects.filter(id__in=ids_to_delete).delete()

            elif form_type == 'tableBody-5':
                # Delete engineer_manager_details records
                EngineerManagerDetails.objects.filter(id__in=ids_to_delete).delete()

            else:
                return JsonResponse({'error': 'Invalid form type'}, status=400)

            return JsonResponse({'success': True, 'message': 'Data deleted successfully'})

        except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

   
    
    return render(request,"app/master.html",context)





def calib(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        if customer_name:
            work_orders = WorkOrder.objects.filter(customer_name=customer_name).distinct().values('work_order_no')
            work_order_list = list(work_orders)
            return JsonResponse(work_order_list, safe=False)
    elif request.method == 'GET':
        work_order_no = request.GET.get('work_order_no')  # Fetch work order number from GET request
        print("work_order_no",work_order_no)
        inward_no = request.GET.get('inward_no')  # Fetch sr_no from GET request
        print('inward_no',inward_no)
        if inward_no:
            try:
                # Fetch the specific item based on sr_no
                work_order = WorkOrder.objects.filter(work_order_no=work_order_no, inward_no=inward_no).first()
                print("work_order",work_order)
                if not work_order:
                    return JsonResponse({'success': False, 'error': 'Item not found.'})

                # Prepare response data for the specific item
                item_data = {
                    'id_no': work_order.id_no,
                    'sr_no': work_order.sr_no,
                    'make': work_order.make,
                    'range': work_order.range,
                    'customer_po_no': work_order.customer_po_no,
                    'customer_ref_date':work_order.customer_ref_date,
                    'inward_no':work_order.inward_no,
                    'inward_date':work_order.wo_date,
                    'channels':work_order.channels,
                    

                }
                print("item_data",item_data)

                return JsonResponse({'success': True, 'item': item_data})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
            

        if work_order_no:
            try:
                work_orders = WorkOrder.objects.filter(work_order_no=work_order_no)
                if not work_orders.exists():
                    return JsonResponse({'success': False, 'error': 'Work order not found.'})

                # Prepare response data
                data = {
                    'success': True,
                    'wo_date': work_orders.first().wo_date,
                    'customer_po_no': work_orders.first().customer_po_no,
                    'customer_ref_date': work_orders.first().customer_ref_date,
                    'order_type': work_orders.first().order_type,
                    'customer_address': work_orders.first().customer_address,
                    'items': []
                }

                for work_order in work_orders:
                    data['items'].append({
                        'inward_no':work_order.inward_no,
                        'item': work_order.item,
                        'hsn': work_order.hsn,
                        'sr_no': work_order.sr_no,
                        'id_no': work_order.id_no,
                        'range': work_order.range,
                        'make': work_order.make
                    })

                return JsonResponse(data)
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        customer_value = Customer.objects.all()
        SettingPlugTrace_value = SettingPlugTrace.objects.all()
        SettingRingTrace_value = SettingRingTrace.objects.all()
        SettingPlugMaster_value = SettingPlugMaster.objects.all()
        SettingRingMaster_value = SettingRingMaster.objects.all()
        EngineerManagerDetails_value = EngineerManagerDetails.objects.all()

    context ={
            'customer_value': customer_value, 
            'SettingPlugTrace_value': SettingPlugTrace_value,
            'SettingRingTrace_value': SettingRingTrace_value,
            'SettingPlugMaster_value' : SettingPlugMaster_value,
            'SettingRingMaster_value' : SettingRingMaster_value,
            'EngineerManagerDetails_value' : EngineerManagerDetails_value
        }
    return render(request,"app/calib.html",context)

def output(request):
    if request.method == 'GET':
        SettingPlugTrace_value = SettingPlugTrace.objects.all()
        SettingRingTrace_value = SettingRingTrace.objects.all()
        SettingPlugMaster_value = SettingPlugMaster.objects.all()
        SettingRingMaster_value = SettingRingMaster.objects.all()

    context ={
            'SettingPlugTrace_value': SettingPlugTrace_value,
            'SettingRingTrace_value': SettingRingTrace_value,
            'SettingPlugMaster_value' : SettingPlugMaster_value,
            'SettingRingMaster_value' : SettingRingMaster_value,
        }
    return render(request,"app/output.html",context)


import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import WorkOrder

def inward(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        if customer_name:
            work_orders = WorkOrder.objects.filter(customer_name=customer_name).distinct().values('work_order_no')
            work_order_list = list(work_orders)
            return JsonResponse(work_order_list, safe=False)

        try:
            data = json.loads(request.body)
            print("The value get from the front end:", data)
            customer_name = data.get('customerName')
            wo_date = data.get('woDate')
            work_order_no = data.get('workOrderNo')
            customer_po_no = data.get('customerPoNo')
            customer_ref_date = data.get('customerRefDate')
            order_type = data.get('orderType')
            customer_address = data.get('customerAddress')

            if not all([customer_name, wo_date, work_order_no]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            items = data.get('items', [])
            saved_items = []
            skipped_items = []

            for item in items:
                sr_no = item.get('srNo')
                id_no = item.get('idNo')
                inward_no = item.get('inward_no')
                
                if sr_no and id_no:
                    # Check if inward_no exists
                    existing_work_order = WorkOrder.objects.filter(inward_no=inward_no).first()

                    if existing_work_order:
                        # Update the existing work order
                        existing_work_order.customer_name = customer_name
                        existing_work_order.wo_date = wo_date
                        existing_work_order.work_order_no = work_order_no
                        existing_work_order.customer_po_no = customer_po_no
                        existing_work_order.customer_ref_date = customer_ref_date
                        existing_work_order.order_type = order_type
                        existing_work_order.customer_address = customer_address
                        existing_work_order.item = item.get('item')
                        existing_work_order.hsn = item.get('hsn')
                        existing_work_order.sr_no = sr_no
                        existing_work_order.id_no = id_no
                        existing_work_order.range = item.get('range')
                        existing_work_order.make = item.get('make')
                        existing_work_order.channels = item.get('channels')
                        existing_work_order.save()  # Save the updated object
                        saved_items.append(existing_work_order.id)  # Optionally collect the IDs of updated records
                    else:
                        # If it doesn't exist, create a new work order
                        work_order = WorkOrder.objects.create(
                            customer_name=customer_name,
                            wo_date=wo_date,
                            work_order_no=work_order_no,
                            customer_po_no=customer_po_no,
                            customer_ref_date=customer_ref_date,
                            order_type=order_type,
                            customer_address=customer_address,
                            inward_no=inward_no,
                            item=item.get('item'),
                            hsn=item.get('hsn'),
                            sr_no=sr_no,
                            id_no=id_no,
                            range=item.get('range'),
                            make=item.get('make'),
                            channels=item.get('channels')
                        )
                        saved_items.append(work_order.id)

            return JsonResponse({
                'message': 'Work order processed successfully!',
                'saved_items': saved_items,
                'skipped_items': skipped_items
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




    elif request.method == 'GET':
        if 'generate_inward_no' in request.GET:
            last_work_order = WorkOrder.objects.order_by('-inward_no').first()
            if last_work_order:
                last_inward_no = last_work_order.inward_no
                match = re.match(r"(SAI/CAL/\d{2}-\d{2}/)(\d+)", last_inward_no)
                if match:
                    prefix = match.group(1)
                    number = int(match.group(2)) + 1
                    new_inward_no = f"{prefix}{number:03d}"
                else:
                    new_inward_no = "SAI/CAL/24-25/001"
            else:
                new_inward_no = "SAI/CAL/24-25/001"
            
            return JsonResponse({'new_inward_no': new_inward_no})
        # Check if we are fetching work order details based on work order number
        work_order_no = request.GET.get('work_order_no')  # Fetch work order number from GET request

        if work_order_no:  # If work order number is provided, fetch related data
            try:
                # Fetch all work orders with the provided work order number
                work_orders = WorkOrder.objects.filter(work_order_no=work_order_no)

                if not work_orders.exists():
                    return JsonResponse({'success': False, 'error': 'Work order not found.'})

                # Prepare response data
                data = {
                    'success': True,
                    'wo_date': work_orders.first().wo_date,  # Assuming wo_date is the same for all items
                    'customer_po_no': work_orders.first().customer_po_no,
                    'customer_ref_date': work_orders.first().customer_ref_date,
                    'order_type': work_orders.first().order_type,
                    'customer_address': work_orders.first().customer_address,
                    'items': []
                }

                # Loop through each work order item and append it to the items list
                for work_order in work_orders:
                    data['items'].append({
                        'inward_no': work_order.inward_no,
                        'item': work_order.item,
                        'hsn': work_order.hsn,
                        'sr_no': work_order.sr_no,
                        'id_no': work_order.id_no,
                        'range': work_order.range,
                        'make': work_order.make,
                        'channels':work_order.channels
                    })

                return JsonResponse(data)

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        # Fetch all Customer objects to pass them to the template for normal GET requests
        customer_value = Customer.objects.all()

        # Render the form with the customer data
        context = {
            'customer_value': customer_value,
        }
        return render(request, "app/inward.html", context)
    
    elif request.method == 'DELETE':
        try:
            # Parse the request body to get the work order ID
            data = json.loads(request.body)
            work_order_id = data.get('work_order_id')
            print("work_order_id",work_order_id)

            if not work_order_id:
                return JsonResponse({'success': False, 'error': 'Missing work order ID.'}, status=400)

            print("Attempting to delete work order with ID:", work_order_id)  # Debug print

            # Find and delete the work order
            work_order = WorkOrder.objects.get(inward_no=work_order_id)
            work_order.delete()

            return JsonResponse({'success': True, 'message': 'Work order deleted successfully!'})

        except WorkOrder.DoesNotExist:
            print("Work order not found with ID:", work_order_id)  # Debug print
            return JsonResponse({'success': False, 'error': 'Work order not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print("Error during deletion:", e)  # Debug print
            return JsonResponse({'success': False, 'error': str(e)}, status=500)



    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


