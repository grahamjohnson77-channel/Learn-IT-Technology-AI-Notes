# Containers

> [!IMPORTANT]
> PLEASE REMEMBER TO DELETE THE AWS RESOURCES AFTER TUTORIAL IS DONE !!!

> [!NOTE]
> Amazon says: AWS App Runner is a fully managed service that makes it easy for developers to quickly deploy containerized web applications and APIs, at scale and with no prior infrastructure experience required. Start with your source code or a container image. App Runner automatically builds and deploys the web application and load balances traffic with encryption. App Runner also scales up or down automatically to meet your traffic needs.

> Be a Better Dev says: Why App Runner? Because Infrastructure is hard. We have to worry about Load Balancing, Target Groups, Autoscaling Groups, Security Groups, Domains, Certificates, Monitors, Logging etc. App Runner takes care of building the infra for us!

> [!TIP]
> The generated resource gets a ARN
> Amazon Resource Names (ARNs) uniquely identify AWS resources. We require an ARN when you need to specify a resource unambiguously across all of AWS, such as in IAM policies, Amazon Relational Database Service (Amazon RDS) tags, and API calls.
> Please read more here:
https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html

> [!IMPORTANT]
> Watch Intros
> https://www.youtube.com/watch?v=DBbvFA6Up98
> https://www.youtube.com/watch?v=TKirecwhJ2c
> Highlights some Issues with AWS App Runner:
> https://www.youtube.com/watch?v=E6E6HtrLs98

> AWS IAM Core Concepts (Roles etc.) from Be a Better Dev Youtube Channel: (Please script to their channel and hit the like)
> https://www.youtube.com/watch?v=_ZCTvmaPgao

# Tutorial Link
https://www.apprunnerworkshop.com/intermediate/container-image/create-service/

Source Used:
https://github.com/aws-containers/hello-app-runner

# Helpful
https://docs.aws.amazon.com/apprunner/
https://aws.amazon.com/blogs/security/how-to-use-trust-policies-with-iam-roles/

https://repost.aws/it/questions/QUhtLYW1B2T_SuGWSlDJVs3Q/guide-to-creating-an-instance-role-that-will-allow-my-app-runner-service-to-use-values-from-ssm-parameter-store

> NOTE: You need to provide this as a trust policy for a App Runner instance role, then this new role would start showing up in the App Runner console ... in the end, I created EC2 app instance and updated the Trushed relationships Tab for the EC2 instance with the following:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "tasks.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

> [!TIP]
> Role (with IAM Policy for App Runner) -> Service -> URL