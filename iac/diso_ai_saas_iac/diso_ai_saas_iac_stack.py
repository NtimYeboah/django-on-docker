from constructs import Construct
from aws_cdk import CfnOutput, Stack, aws_ec2 as ec2


class DisoAiSaasIacStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)],
        )

        # Security group
        security_group = ec2.SecurityGroup(self, "DisoSecurityGroup", vpc=vpc)

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP connections from the world")
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow HTTPS connections from the world"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "Allow Postgress connections from the world"
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH connections from the world")

        cfn_key_pair = ec2.CfnKeyPair(
            self,
            "disoWebServerKey",
            key_name="disoWebServerKey",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCa7Fo6FCgYqj/PuCjzC/X9E7wwFmL5WaM8eIveBIsGwzvnwkUgf2Y1Sc4mq30kDdFYU9rjT/oid1sesJ1RGWVXcsx50WIswVwkusFM7Nqgxf+vf7lY/LQSOprXnf6GyLl6U2UsoqGRYqXRl2Cw825DUCFvWOcbo442uQReuMhO72dvQgczqR6Vm4DFv4aQxrxWGlWkV+NwQTQe1ECP8N8KibNMtGu+WrT4DwN97yDoeMcWs34hGWFLzoVS2bDjmEeBSNaJs+w09Qt1Mk/8rvENLH60eA4E1zi8KF8fuqFgMf0cUN+ZU5//OgZE9Lmmr9Wb+pFmDl6u/QL83FiBTaiaS/jLGyVpiAEsWnLr5HfOh/1n8MD7rJMDrD9mjTuXmo1p8CsVY6/j/7UftjIVzfj5YRoTToU2IWfkdkVAtaoe/l2XqadsnoPY519wmtuRRQISAHMjaeQYt/USuzV5mcjaY6J75YS8ubNnVJDtbjA+5Ei5pPVscLffp666JQ7LEPWov9w+jnbA/midb35f4gAw+qqt0lU+/jgjUhj/ApD73+WS/zZQkGYGsM6fhrlxfycqjDCr1mTy9DaLiY/0yhwtu3npyKeU/Jd24TIQlhYkeSVMvXu24OpX6BL3jet/9UdBBdh912IkGF4+HGPsEj/fm7ouJX/ILSc2VyQPQvlwgQ== ntimyeboah@ntims-macbook-pro.local",
        )

        # Instance
        instance = ec2.Instance(
            self,
            "Diso_Web_Server",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=security_group,
            key_name=cfn_key_pair.key_name,
        )

        # Output the public IP address
        CfnOutput(self, "InstanceId", value=instance.instance_id)
        CfnOutput(self, "InstancePublicIp", value=instance.instance_public_ip)
