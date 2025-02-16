#!/usr/bin/env python3

import aws_cdk as cdk

from diso_ai_saas_iac.diso_ai_saas_iac_stack import DisoAiSaasIacStack


app = cdk.App()
DisoAiSaasIacStack(app, "DisoAiSaasIacStack")

app.synth()
