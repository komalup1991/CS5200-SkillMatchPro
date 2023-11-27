from django.shortcuts import render, redirect
from django.views import View
from .forms import DisputeForm
from userInfo.models import UserInfo, Project

class RaiseDisputeView(View):
    template_name = 'dispute/raise_dispute.html'

    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        form = DisputeForm()
        return render(request, self.template_name, {'form': form, 'project': project})

    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        form = DisputeForm(request.POST)
        
        if form.is_valid():
            dispute = form.save(commit=False)
            
            # Retrieve the UserInfo instance based on the user ID
            user_id = request.session.get('user_id')
            from_user = UserInfo.objects.get(userID=user_id)
            to_user = UserInfo.objects.get(userID=project.freelancerID)
            
            dispute.from_user = from_user
            dispute.to_user = to_user
            dispute.project =  Project.objects.get(projectID=project.projectID)
            dispute.dispute_status = 'active'  
            dispute.save()
            return redirect('dispute_success') 
        
        return render(request, self.template_name, {'form': form, 'project': project})
    
def dispute_success(request):
    return render(request, 'dispute/dispute_success.html')
