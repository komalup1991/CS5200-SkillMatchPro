from django.views import View
from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime
from .models import Rating,Userinfo,Project

class RatingView(View):
    template_name = 'rating/rating_form.html'
    initial_comment = "Perfect experience! I love skillMatchPro!!!"
    star = 3
    date = datetime.now()
    userid = 0
    ratedReceiver = 0 

    def get(self, request, project_id):
        userid = request.session.get('user_id')  # Move this line inside the get method
        self.userid = userid
        self.project_id = project_id
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                    projectID,title,freelancerID,bidderID
                    FROM
                    Project
                    where projectID = %s
                    ;
                """,[project_id])

            # Fetch all results from the cursor
            curProject = cursor.fetchall()

        if(userid == curProject[0][2]): # user is freelancerID
            rateReceiver =  curProject[0][3]
        elif (userid == curProject[0][3] ):
            rateReceiver = curProject[0][2]
        self.ratedReceiver = rateReceiver

        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                    userID, name , specialization
                    FROM
                    UserInfo
                    where userID = %s
                    ;
                """,[rateReceiver])

            # Fetch ratedUser info from the cursor
            rateObj = cursor.fetchall()

        # check has rated this retaReceiver by rater about this project before
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                rating, comment, date
                FROM
                Rating
                WHERE ratedUserID = %s
                    AND ratingByUserID = %s
                    AND projectid = %s
                ;
            """, [rateReceiver, userid, project_id])

            rated = cursor.fetchall()

        hasRated = False
        if rated:
            hasRated = True
            self.star = rated[0][0]
            self.initial_comment = rated[0][1]
            self.date = rated[0][2]
        print(hasRated)
        context = {"curProject" : curProject, 
                   "rateReceiver": rateObj, 
                   'hasRated': hasRated,
                   'initial_comment': self.initial_comment,
                   'star': self.star,
                   'date': self.date
                   }

        return render(request, self.template_name, context)

    def post(self, request, project_id):
        userid = request.session.get('user_id')  # Move this line inside the get method
        self.userid = userid

        date = datetime.now()
        star = request.POST.get("star")

        comment = request.POST.get("comment").strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                    projectID,title,freelancerID,bidderID
                    FROM
                    Project
                    where projectID = %s
                    ;
                """,[project_id])

            # Fetch all results from the cursor
            curProject = cursor.fetchall()

        rateReceiver = 0
        if(userid == curProject[0][2]): # user is freelancerID
            rateReceiver =  curProject[0][3]
        elif (userid == curProject[0][3] ):
            rateReceiver = curProject[0][2]

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                rating, comment, date
                FROM
                Rating
                WHERE ratedUserID = %s
                    AND ratingByUserID = %s
                    AND projectid = %s
                ;
            """, [rateReceiver, userid, project_id])

            rated = cursor.fetchall()
            
        hasRated = False
        if rated:
            hasRated = True
            self.star = rated[0][0]
            self.initial_comment = rated[0][1]
            self.date = rated[0][2]

        if (hasRated == True):
            # Handle update logic
            Rating.objects.filter(
                rateduserid=Userinfo.objects.get(userid=rateReceiver),
                ratingbyuserid=Userinfo.objects.get(userid=self.userid),
                projectid=Project.objects.get(projectid=project_id)
            ).update(
                rating=star,
                comment=comment,
                date=date,
    )
        else:
            # Handle create logic
            Rating.objects.create(
                       rateduserid = Userinfo.objects.get(userid=rateReceiver),
                       ratingbyuserid = Userinfo.objects.get(userid=self.userid),
                       rating = star,
                       comment = comment,
                       date = date,
                       projectid = Project.objects.get(projectid= project_id)
                           )

        return redirect('../../project/projectlist/'+ str(project_id))
