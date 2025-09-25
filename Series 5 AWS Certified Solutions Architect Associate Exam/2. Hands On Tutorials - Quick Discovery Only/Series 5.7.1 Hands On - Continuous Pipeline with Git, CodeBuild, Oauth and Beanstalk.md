# Compute Category

> [!IMPORTANT]
> PLEASE REMEMBER TO DELETE THE AWS RESOURCES AFTER TUTORIAL IS DONE !!!

> [!NOTE]
> Amazon says: In this tutorial, you will create a continuous delivery pipeline for a simple web application. You will first use a version control system to store your source code. Then, you will learn how to create a continuous delivery pipeline that will automatically deploy your web application whenever your source code is updated.

> AWS Elastic Beanstalk is a compute service that makes it easy to deploy and manage applications on AWS without having to worry about the infrastructure that runs them.

> You will use AWS CodeBuild to build the source code previously stored in your GitHub repository. AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy.

> OAuth—Open protocol for secure authorization. OAuth enables you to connect your GitHub account to third-party applications, including AWS CodeBuild.

> You will use AWS CodePipeline to set up a continuous delivery pipeline with source, build, and deploy stages. The pipeline will detect changes in the code stored in your GitHub repository, build the source code using AWS CodeBuild, and then deploy your application to AWS Elastic Beanstalk.

> You will use AWS CodePipeline to add a review stage to your countinuous delivery pipeline.

> As part of this process, you can add an approval action to a stage at the point where you want the pipeline execution to stop so someone can manually approve or reject the action. Manual approvals are useful to have someone else review a change before deployment. If the action is approved, the pipeline execution resumes. If the action is rejected—or if no one approves or rejects the action within seven days—the result is the same as the action failing, and the pipeline execution does not continue.

> [!IMPORTANT]
> Watch Intros
>

# Tutorial Link
https://aws.amazon.com/getting-started/hands-on/create-continuous-delivery-pipeline/?ref=gsrchandson

# Read More
https://kekayan.medium.com/redis-on-aws-36ed7054357e

# Helpful
<br> https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-iam-instance-profile.html#getting-started-create-iam-instance-profile-console