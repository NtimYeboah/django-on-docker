import aws_cdk as core
import aws_cdk.assertions as assertions
from diso_ai_saas_iac.diso_ai_saas_iac_stack import DisoAiSaasIacStack


def test_ec2_instance_created():
    app = core.App()
    stack = DisoAiSaasIacStack(app, "diso-ai-saas-iac")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::EC2::VPC", 1)

    template.has_resource_properties("AWS::EC2::Subnet", {"MapPublicIpOnLaunch": True})

    template.resource_count_is("AWS::EC2::SecurityGroup", 1)
    template.has_resource_properties(
        "AWS::EC2::SecurityGroup",
        {
            "SecurityGroupIngress": [
                {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "CidrIp": "0.0.0.0/0"},
                {"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "CidrIp": "0.0.0.0/0"},
                {"IpProtocol": "tcp", "FromPort": 5432, "ToPort": 5432, "CidrIp": "0.0.0.0/0"},
                {"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "CidrIp": "0.0.0.0/0"},
            ]
        },
    )

    template.resource_count_is("AWS::EC2::Instance", 1)
    template.has_resource_properties(
        "AWS::EC2::Instance",
        {
            "InstanceType": "t2.micro",
        },
    )
