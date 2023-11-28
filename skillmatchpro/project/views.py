from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView,DetailView,CreateView
from .models import Project,Bid,Userinfo,Category
from django.db import connection
from datetime import datetime
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.


class Index(View):
    def get(self,request):
        return render(request, 'project/project_list.html')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    maxBid = 0

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Category.name, Project.title, Project.projectStatus, Project.description, Project.photo, Project.budget, Project.projectID, Project.freelancerID,Project.bidderID
                FROM Project
                LEFT JOIN Category ON Project.categoryID = Category.categoryID
                WHERE Project.projectID = %s
                ;
            """, [self.kwargs['project_id']])

            # Fetch all results from the cursor
            projects_detail = cursor.fetchall()

            cursor.execute("""
                SELECT max(Bid.amount), projectID
                FROM Bid
                WHERE Bid.projectID = %s
                ;
            """, [self.kwargs['project_id']])
            max_bid = cursor.fetchall()
            self.maxBid = max_bid[0][1]

            cursor.execute("""
                SELECT bidID, amount, status, date
                FROM Bid
                WHERE Bid.projectID = %s
                ;
            """, [self.kwargs['project_id']])
            bids = cursor.fetchall()

        context['data'] = projects_detail
        context['maxBid'] = max_bid
        context['bids'] = bids

        #check user's relationship with project
        userid = self.request.session.get('user_id')
            
        if((projects_detail[0][7] == userid or projects_detail[0][8] == userid) and projects_detail[0][2] == "completed"):
            isRate = "Y"
        else:
            isRate = "N"
        if(projects_detail[0][2] == "active"):
            isMessage = "Y"
            isStatus = "Y"
        else:
            isMessage = "N"
            isStatus = "N"

        if(projects_detail[0][2] == "active" and projects_detail[0][7] != userid):
            isBid = "Y"
        else:
            isBid = "N"
        context["isRate"] = isRate
        context["isMessage"] = isMessage
        context["isStatus"] = isStatus
        context["isBid"] = isBid
        # print(isStatus)
        # print(isRate)
        # print(isBid)
        # print(isMessage)
        return context
    
    def quickBid(self, **kwargs):
        bid = Bid()
        bid.userid = 1
        bid.amount = 800
        bid.projectid = self.kwargs['project_id']
        bid.save()
        return HttpResponse("Successful")

    
class ProjectList(ListView): 
    template_name='project/project_list.html' 
    model = Project


class ProjecDetail(DetailView): 
    model = Project



    
def deleteBid(bidID):
    Bid.objects.filter(bidid=bidID).delete()
    data_list = Bid.objects.all()


def ProjectAdd(request):
    if request.method == "GET":
        """ Add project"""
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                    Category.categoryid,Category.name
                    FROM
                    Category
                    ;
                """)

                # Fetch all results from the cursor
            category = cursor.fetchall()
        context = {"data" : category}

        
        return render(request,'project/project_add.html', context)
    
    # Else Get user post data for submit
    title = request.POST.get("title")
    description = request.POST.get("description")
    target = request.POST.get("target")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    
    userid = request.session.get('user_id')
    user_instance = Userinfo.objects.get(userid=userid)

    projectID = Project.objects.count()+1

    status = 'active'

    selected_category = request.POST.get('gridRadios')
    category_instance = Category.objects.get(name  = selected_category)
    url = request.FILES
    if url:
        p = url.get("file")
        new_filename = str(uuid.uuid4()) + os.path.splitext(p.name)[-1]
        u = os.path.abspath(__file__) # cur photo abs path
        u = os.path.dirname(u)
        newdir = "/static/project/img/"
        u = u + newdir

        # upload_dir = u
        u = os.path.join(u,new_filename)
        
        with open(u,'wb') as f:
            for x in p.chunks():
                f.write(x)
        photo = 'project/img/' + new_filename
    else:
        photo = ''
    # uploaded_file = p
    
    
    # fs = FileSystemStorage()
    # upload_dir = settings.MEDIA_ROOT
    # filename = fs.save(os.path.join(upload_dir, uploaded_file.name), uploaded_file)
    # file_url = fs.url(filename)
    # print(file_url)


    # store in database
    Project.objects.create(title = title,description = description,budget = target,
                           deadline = enddate, 
                           startdate = startdate,
                           freelancerid = user_instance,
                           projectid = projectID,
                           projectstatus = status,
                           categoryid = category_instance,
                           photo = photo
        )

    return redirect('../../my-projects/')


def bidAdd(request,project_id,max_bid):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                    projectID,title
                    FROM
                    Project
                    where projectID = %s
                    ;
                """,[project_id])

                # Fetch all results from the cursor
            curProject = cursor.fetchall()
        context = {"curProject" : curProject}
        print("maxbid" , max_bid)
        if(max_bid == "None"):
            context['max_bid']  = 100
        else:
            context['max_bid'] = float(max_bid) + 1
        return render(request,'project/bid_form.html', context)
    
    amount = request.POST.get("amount")
    bidID = Bid.objects.count()+1
    userid = request.session.get('user_id')
    user_instance = Userinfo.objects.get(userid=userid)

    project_instance = Project.objects.get(projectid=project_id)
    date = datetime.now()
    Bid.objects.create(bidid= bidID,
                       userid = user_instance,
                       projectid = project_instance,
                       amount = amount,
                       date = date
                           )

    return redirect('../../projectlist/'+ str(project_id))








