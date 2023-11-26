from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.views.generic import ListView,DetailView,CreateView
from .models import Project,Bid,Userinfo,Category
from django.db import connection
from django.urls import reverse
from datetime import datetime
from django.http import HttpResponseRedirect
import qiniu
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Category.name, Project.title, Project.projectStatus, Project.description, Project.photo, Project.budget, Project.projectID
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

        return context
    
    def quickBid(self, request, **kwargs):
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


# class ProjectAdd():
#     model = Project
#     template_name = 'project/project_add.html'
#     context_object_name = 'project'
#     pk_url_kwarg = 'project_id'

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
    

    userid = 1
    user_instance = Userinfo.objects.get(userid=userid)

    projectID = Project.objects.count()+1

    status = 'active'

    selected_category = request.POST.get('gridRadios')
    category_instance = Category.objects.get(name  = selected_category)

    # store in database
    Project.objects.create(title = title,description = description,budget = target,
                           deadline = enddate, 
                           startdate = startdate,
                           freelancerid = user_instance,
                           projectid = projectID,
                           projectstatus = status,
                           categoryid = category_instance
                           )


    # redirect to projectlist
    return redirect('./')


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
        context['max_bid'] = max_bid
        return render(request,'project/bid_form.html', context)
    
    amount = request.POST.get("amount")
    bidID = Bid.objects.count()+1

    userid = 2
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


# @require_GET
# def qntoken(request):
#     access_key = 'r**********5'
#     secret_key = 'v**********t'
#     q = Auth(access_key, secret_key)
#     key = "database5200" + str(datetime.now())
#     bucket_name = 'pygr'  
#     token = q.upload_token(    bucket_name ,key,3600)
#     # upload
#     localfile = './sync/bbb.jpg'
#     ret, info = put_file(token, key, localfile, version='v2') 
#     print(info)
#     assert ret['key'] == key
#     assert ret['hash'] == etag(localfile)
#     return ret["key"]






