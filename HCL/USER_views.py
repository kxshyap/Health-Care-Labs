from django.shortcuts import render,redirect

from HealthCareLabs import settings

from .forms import signupForm,testForm,contactForm
from .models import user_info,test_info,contact_info
from django.contrib.auth import logout
# from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
import random
from django.core.mail import send_mail, EmailMessage
import os
from django.http import FileResponse,HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.


# def encryptPassword(password):
#     key=Fernet.generate_key()
#     fernet=Fernet(key)
#     encpassword=fernet.encrypt(password.encode())
#     return encpassword

# def decryptPassword(password):
#     key=Fernet.generate_key()
#     fernet=Fernet(key)
#     decpassword=fernet.decrypt(password).decode()
#     return decpassword


def index(request):

    if request.session.get('is_logged_in'):
        user = {
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }
    else:
        user = None

    if request.method=='POST': #root

        # Signup
        if request.POST.get('signup')=='signup':
            emailid=''
            newuser=signupForm(request.POST)
            # data = request.POST
            if newuser.is_valid():
                fname=newuser.cleaned_data.get('fname')
                lname=newuser.cleaned_data.get('lname')
                emailid=newuser.cleaned_data.get('email')
                # encrypted_Password=encryptPassword(data.get('password'))
                try:
                    em=user_info.objects.get(email=emailid)
                    print('\nEmail Address already in use.\n')
                except user_info.DoesNotExist:
                    # newuser = user_info(fname=data.get('fname'),lname=data.get('lname'),uname=data.get('uname'),
                    # email=data.get('email'),password=encrypted_Password,mobile=data.get('mobile'),zip=data.get('zip'),
                    # city=data.get('city')
                    # )
                    newuser.save()
                    print("\nUser created successfully!\n")
                    messages.success(request, f'Account created for {fname} {lname}!')
                    return redirect('user_account')
            else:
                print(newuser.errors)

        # Login
        elif request.POST.get('login')=='login':
            emid=request.POST['email']
            pas=request.POST['password']
            # enpassword=encryptPassword(pas)
            user=user_info.objects.filter(email=emid,password=pas)
            uid=user_info.objects.get(email=emid)
            print("UserID:",uid.id)

            if user: #true
                    print("Login Successfull!")
                    request.session['user']=emid
                    request.session['userid']=uid.id
    
                    return redirect('user_account')
            else:
                print("Error! Email or Password does't match.")
    return render(request,'index.html',{'user':user})

def forget_password(request):

    if request.session.get('is_logged_in'):
        user = {
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }
    else:
        user = None
        user_mail=None

    otp = None
    if request.method=='POST':

        # OTP Generation
        if request.POST.get('generate_otp')=='generate_otp':
            user_mail=request.POST['email']
            user_check=user_info.objects.filter(email=user_mail)
            cuser=user_info.objects.get(email=user_mail)
            
            if user_check: #true
                #Email Sending Code
                otp = random.randint(100000,999999)
                fnm=cuser.fname
                lnm=cuser.lname
                sub='Password reset request for HealthCareLabs'
                msg=f'Dear, {fnm} {lnm}\n\n{otp} is your verification code for generating a new password.'
                to_ID=[user_mail]
                send_mail(subject=sub, message=msg, from_email=settings.EMAIL_HOST_USER, recipient_list=to_ID)
                messages.success(request,'An OTP has been sent to your registered email.')

                # Submit New Password
                if request.POST.get('set_password')=='set_password':
                    input_otp = request.POST['otp']
                    new_password = request.POST['new_password']
                    confirm_password = request.POST['confirm_password']

                    if input_otp.get('otp') == otp and new_password == confirm_password:

                        updatepassword=signupForm(request.POST)
                        if updatepassword.is_valid():
                            updatepassword.save()
                            print('\nYour password has been updated.\n')
                            messages.success(request,'Your password has been updated.')
                            return redirect('index')
                        else:
                            print(updatepassword.errors)

        return render(request,'forget_password.html',{'user':user,'cuser':user_info.objects.get(email=user_mail)})


def updateprofile(request):
    user=request.session.get('user')
    uid=request.session.get('userid')
    cuser=user_info.objects.get(id=uid)
    if request.method=='POST':
        updateuser=signupForm(request.POST)
        if updateuser.is_valid():
            updateuser=signupForm(request.POST,instance=cuser)
            updateuser.save()
            print('\nYour profile has been updated.\n')
            messages.warning(request,'Your profile has been updated.')
            return redirect('user_account')
        else:
            print(updateuser.errors)
    return render(request,'updateprofile.html',{'user':user,'cuser':user_info.objects.get(id=uid)})


def userlogout(request):
    logout(request)
    messages.info(request,'You have been logged out.')
    return redirect('/')


def user_account(request):
    user=request.session.get('user')
    uid=request.session.get('userid')
    cuser=user_info.objects.get(id=uid)
    user_tests=test_info.objects.filter(email=user)
    return render(request,'user_account.html',{'user':user,'cuser':user_info.objects.get(id=uid),'user_tests':user_tests})


def test_booking(request):
    user=request.session.get('user')
    uid=request.session.get('userid')
    cuser=user_info.objects.get(id=uid)
    tests={'Complete Blood Count (CBC) - EDTA Whole Blood': 300,
    'Blood Glucose Test (HBA1c)': 400 ,'Kidney Function Test (KFT)': 500,
    'Liver Function Test (LFT)': 450 ,'Covid RT PCR': 600,
    'Blood Group': 400 ,'Haemoglobin (Hb)': 200,}

    if request.method=='POST':
        new_test=testForm(request.POST,request.FILES)
        if new_test.is_valid():
            new_test_instance = new_test.save(commit=False)
            new_test_instance.save()
            test_id = new_test_instance.id
            new_test_data = test_info.objects.get(id=test_id)
            user_id = cuser.id
            # Email Sending
            test_data = {
                'app_no':   f'Application Number: # {test_id}',
                'pat_name': f'Patient Name: {new_test_data.fname} {new_test_data.lname}',
                'pat_age':  f'Age: {new_test_data.age}',
                'gender':   f'Gender: {new_test_data.gender}',
                't_name':   f'Test Name: {new_test_data.testname}',
                'date_time':f'Scheduled Date and Time: {new_test_data.test_date}, {new_test_data.test_time}',
                'price':    f'Test Price: Rs. {new_test_data.test_price}',
                'mode':     f'Mode of Payment: {new_test_data.mop}',
            }
            fnm=cuser.fname
            lnm=cuser.lname
            sub='Test Booking Details'
            msg=f"""Dear {fnm} {lnm},\n\nYour test has been successfully booked.\n
            Application Number: #{test_id}\n
            Patient Name: {new_test_data.fname} {new_test_data.lname}\n
            Age: {new_test_data.age}\n
            Gender: {new_test_data.gender}\n
            Test Name: {new_test_data.testname}\n
            Test Date and Time: {new_test_data.test_date}, {new_test_data.test_time}\n
            Test Price: {new_test_data.test_price}\n
            Mode of Payment: {new_test_data.mop}\n\n
            For any enquiries please contact us at +91 1234567890 or info.healthcarelabs@gmail.com
            """
            to_ID=[new_test_data.email]
            send_mail(subject=sub, message=msg, from_email=settings.EMAIL_HOST_USER, recipient_list=to_ID)
            # print(test_id, user_id)
            # generate_pdf = report_PDF('report.html',test_data)
            # # return HttpResponse(generate_pdf, content_type='application/pdf') # Optional Download

            # if generate_pdf: # Force Download
            #     response = HttpResponse(generate_pdf, content_type='application/pdf')
            #     filename = f'{cuser.fname} {cuser.lname}_{test_id}'
            #     content = f'inline; filename={filename}'
            #     content = f'attachment; filename={filename}'
            #     response['Content-Disposition'] = content
            #     print('PDF Generated.')
            #     return response
            print('\nNew test has been generated.\n')
            messages.success(request,'New test has been generated.')
            return redirect(user_account)

        else:
            print(new_test.errors)

    return render(request,'test_booking.html',{'tests':tests,'user':user,'cuser':user_info.objects.get(id=uid)})


# def report_PDF(template_src,context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')),result)
#     if pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None
#     # # Add test info in pdf
#     # lines = []
    
#     # lines.append(f'=======================================================================================')
#     # lines.append(f'Application Number: # {test_id}')
#     # lines.append(f'Patient Name: {userinfo.fname} {userinfo.lname}')
#     # lines.append(f'Age: {testinfo.age}')
#     # lines.append(f'Gender: {testinfo.gender}')
#     # lines.append(f'Test Name: {testinfo.testname}')
#     # lines.append(f'Scheduled Date and Time: {testinfo.test_date}, {testinfo.test_time}')
#     # lines.append(f'Test Price: {testinfo.test_price}')
#     # lines.append(f'Mode of Payment: {testinfo.mop}')
#     # lines.append(f'For any enquiries please contact us at +91 1234567890 or info.healthcarelabs@gmail.com')
#     # lines.append(f'=======================================================================================')

#     # for line in lines:
#     #     textob.textLine(line)

#     # c.drawText(textob)
#     # c.showPage()
#     # c.save()
#     # print('PDF Generated.')
#     # buf.seek(0)
    
#     # # email = EmailMessage(
#     # # subject='Test Booking Successful',
#     # # body=f'Dear {userinfo.fname} {userinfo.lname},\n PLease find your test booking details in the attachment.',
#     # # from_email=settings.EMAIL_HOST_USER,
#     # # to=[userinfo.email]
#     # # )
#     # file_name = f"{userinfo.fname}_{userinfo.lname}_{test_id}.pdf"
#     # # pdf_file_path = os.path.join(settings.MEDIA_ROOT, "pdf", file_name)
#     # # email.attach_file(pdf_file_path)

#     # # # send the email
#     # # email.send()
#     # # response = HttpResponse(buf.read(), content_type='application/pdf')
#     # # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
#     # return FileResponse(buf, as_attachment=True, filename=f'{file_name}')


def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method=='POST':
        new_message=contactForm(request.POST)
        if new_message.is_valid():
            new_message.save()
            print('\nNew comment has been posted.\n')
    return render(request,'contact.html')



def pricing(request):
    tests={'Complete Blood Count (CBC) - EDTA Whole Blood': 300,
    'Blood Glucose Test (HBA1c)': 400 ,'Kidney Function Test (KFT)': 500,
    'Liver Function Test (LFT)': 450 ,'Covid RT PCR': 600,
    'Blood Group': 400 ,'Haemoglobin (Hb)': 200,}

    return render(request,'pricing.html',{'tests':tests})

