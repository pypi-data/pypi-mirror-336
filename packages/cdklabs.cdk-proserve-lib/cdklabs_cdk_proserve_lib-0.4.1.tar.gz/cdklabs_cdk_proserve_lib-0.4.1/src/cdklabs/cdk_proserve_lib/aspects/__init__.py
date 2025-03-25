from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8
from ..types import LambdaConfiguration as _LambdaConfiguration_9f8afc24


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.AlarmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "metric_name": "metricName",
        "period": "period",
        "statistic": "statistic",
        "threshold": "threshold",
    },
)
class AlarmConfig:
    def __init__(
        self,
        *,
        comparison_operator: _aws_cdk_aws_cloudwatch_ceddda9d.ComparisonOperator,
        datapoints_to_alarm: jsii.Number,
        evaluation_periods: jsii.Number,
        metric_name: "Ec2AutomatedShutdown.Ec2MetricName",
        period: _aws_cdk_ceddda9d.Duration,
        statistic: builtins.str,
        threshold: jsii.Number,
    ) -> None:
        '''(experimental) Optional custom metric configuration for CloudWatch Alarms.

        If not provided, defaults to CPU utilization with a 5% threshold.

        :param comparison_operator: (experimental) The comparison operator to use for the alarm. Default: = ComparisonOperator.LESS_THAN_THRESHOLD
        :param datapoints_to_alarm: (experimental) The number of datapoints that must go past/below the threshold to trigger the alarm. Default: = 2
        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold. Default: = 3
        :param metric_name: (experimental) The name of the CloudWatch metric to monitor. Default: = CPUUtilization
        :param period: (experimental) The period over which the metric is measured. Default: = 1 minute
        :param statistic: (experimental) The CloudWatch metric statistic to use. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Default: = 'Average'
        :param threshold: (experimental) The threshold value for the alarm. Default: = 5%

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e80c1625a9aebade1607b9063a75a5e101289462594aab3e82799e39c067ab)
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "datapoints_to_alarm": datapoints_to_alarm,
            "evaluation_periods": evaluation_periods,
            "metric_name": metric_name,
            "period": period,
            "statistic": statistic,
            "threshold": threshold,
        }

    @builtins.property
    def comparison_operator(
        self,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.ComparisonOperator:
        '''(experimental) The comparison operator to use for the alarm.

        :default: = ComparisonOperator.LESS_THAN_THRESHOLD

        :stability: experimental
        '''
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.ComparisonOperator, result)

    @builtins.property
    def datapoints_to_alarm(self) -> jsii.Number:
        '''(experimental) The number of datapoints that must go past/below the threshold to trigger the alarm.

        :default: = 2

        :stability: experimental
        '''
        result = self._values.get("datapoints_to_alarm")
        assert result is not None, "Required property 'datapoints_to_alarm' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''(experimental) The number of periods over which data is compared to the specified threshold.

        :default: = 3

        :stability: experimental
        '''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metric_name(self) -> "Ec2AutomatedShutdown.Ec2MetricName":
        '''(experimental) The name of the CloudWatch metric to monitor.

        :default: = CPUUtilization

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast("Ec2AutomatedShutdown.Ec2MetricName", result)

    @builtins.property
    def period(self) -> _aws_cdk_ceddda9d.Duration:
        '''(experimental) The period over which the metric is measured.

        :default: = 1 minute

        :stability: experimental
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def statistic(self) -> builtins.str:
        '''(experimental) The CloudWatch metric statistic to use.

        Use the ``aws_cloudwatch.Stats`` helper class to construct valid input
        strings.

        :default: = 'Average'

        :stability: experimental
        '''
        result = self._values.get("statistic")
        assert result is not None, "Required property 'statistic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(experimental) The threshold value for the alarm.

        :default: = 5%

        :stability: experimental
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class ApplyRemovalPolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.ApplyRemovalPolicy",
):
    '''(experimental) Sets a user specified Removal Policy to all resources that the aspect applies to.

    This Aspect is useful if you want to enforce a specified removal policy on
    resources. For example, you could ensure that your removal policy is always
    set to RETAIN or DESTROY.

    :stability: experimental

    Example::

        import { App, Aspects, RemovalPolicy } from 'aws-cdk-lib';
        import { ApplyRemovalPolicy } from '@cdklabs/cdk-proserve-lib/aspects';
        
        const app = new App();
        
        Aspects.of(app).add(
          new ApplyRemovalPolicy({ removalPolicy: RemovalPolicy.DESTROY })
        );
    '''

    def __init__(self, *, removal_policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''(experimental) Creates a new instance of SetRemovalPolicy.

        :param removal_policy: (experimental) The removal policy to apply to the resource.

        :stability: experimental
        '''
        props = ApplyRemovalPolicyProps(removal_policy=removal_policy)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visits a construct and applies the removal policy.

        :param node: The construct being visited.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ce1ca35633c77f43304cf7f1782f1ebf1496f151645dca582fc865fe0fe866)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.ApplyRemovalPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"removal_policy": "removalPolicy"},
)
class ApplyRemovalPolicyProps:
    def __init__(self, *, removal_policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''(experimental) Properties for configuring the removal policy settings.

        :param removal_policy: (experimental) The removal policy to apply to the resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858f2996365d3ec27b04534ec073a42ea6b65c3aa7cc1fa650e2765c14c83528)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "removal_policy": removal_policy,
        }

    @builtins.property
    def removal_policy(self) -> _aws_cdk_ceddda9d.RemovalPolicy:
        '''(experimental) The removal policy to apply to the resource.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        assert result is not None, "Required property 'removal_policy' is missing"
        return typing.cast(_aws_cdk_ceddda9d.RemovalPolicy, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplyRemovalPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class CreateLambdaLogGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.CreateLambdaLogGroup",
):
    '''(experimental) Ensures that Lambda log groups are created for all Lambda functions that the aspect applies to.

    :stability: experimental

    Example::

        import { App, Aspects } from 'aws-cdk-lib';
        import { CreateLambdaLogGroup } from '@cdklabs/cdk-proserve-lib/aspects';
        
        const app = new App();
        
        Aspects.of(app).add(new CreateLambdaLogGroup());
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visits a construct and creates a log group if the construct is a Lambda function.

        :param node: The construct being visited.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6b301934b30a296211f1f67b29307771270f03bbb136c1415e30d55396295a)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class Ec2AutomatedShutdown(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.Ec2AutomatedShutdown",
):
    '''(experimental) Automatically shut down EC2 instances when an alarm is triggered based off of a provided metric.

    🚩 If you are applying this Aspect to multiple EC2 instances, you
    will need to configure the CDK context variable flag
    ``@aws-cdk/aws-cloudwatch-actions:changeLambdaPermissionLogicalIdForLambdaAction``
    set to ``true``. If this is not configured, applying this Aspect to multiple
    EC2 instances will result in a CDK synth error.

    Allows for cost optimization and the reduction of resources not being
    actively used. When the EC2 alarm is triggered for a given EC2 instance, it
    will automatically trigger a Lambda function to shutdown the instance.

    :stability: experimental

    Example::

        import { App, Aspects, Duration, Stack } from 'aws-cdk-lib';
        import { ComparisonOperator, Stats } from 'aws-cdk-lib/aws-cloudwatch';
        import { Instance } from 'aws-cdk-lib/aws-ec2';
        import { Ec2AutomatedShutdown } from './src/aspects/ec2-automated-shutdown';
        
        const app = new App({
            context: {
                '@aws-cdk/aws-cloudwatch-actions:changeLambdaPermissionLogicalIdForLambdaAction':
                    true
            }
        });
        const stack = new Stack(app, 'MyStack');
        
        // Create your EC2 instance(s)
        const instance = new Instance(stack, 'MyInstance', {
            // instance properties
        });
        
        // Apply the aspect to automatically shut down the EC2 instance when underutilized
        Aspects.of(stack).add(new Ec2AutomatedShutdown());
        
        // Or with custom configuration
        Aspects.of(stack).add(
            new Ec2AutomatedShutdown({
                alarmConfig: {
                    metricName: Ec2AutomatedShutdown.Ec2MetricName.NETWORK_IN,
                    period: Duration.minutes(5),
                    statistic: Stats.AVERAGE,
                    threshold: 100, // 100 bytes
                    evaluationPeriods: 6,
                    datapointsToAlarm: 5,
                    comparisonOperator: ComparisonOperator.LESS_THAN_THRESHOLD
                }
            })
        );
    '''

    def __init__(
        self,
        *,
        alarm_config: typing.Optional[typing.Union[AlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_9f8afc24, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alarm_config: (experimental) Optional custom metric configuration. If not provided, defaults to CPU utilization with a 5% threshold.
        :param encryption: (experimental) Optional KMS Encryption Key to use for encrypting resources.
        :param lambda_configuration: (experimental) Optional Lambda configuration settings.

        :stability: experimental
        '''
        props = Ec2AutomatedShutdownProps(
            alarm_config=alarm_config,
            encryption=encryption,
            lambda_configuration=lambda_configuration,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5994fe93c71f1c46730fa11383aefb416e003558c08ffb0724aa66546df71bf)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @jsii.enum(
        jsii_type="@cdklabs/cdk-proserve-lib.aspects.Ec2AutomatedShutdown.Ec2MetricName"
    )
    class Ec2MetricName(enum.Enum):
        '''(experimental) CloudWatch Alarm Metric Names.

        :stability: experimental
        '''

        CPU_UTILIZATION = "CPU_UTILIZATION"
        '''
        :stability: experimental
        '''
        DISK_READ_OPS = "DISK_READ_OPS"
        '''
        :stability: experimental
        '''
        DISK_WRITE_OPS = "DISK_WRITE_OPS"
        '''
        :stability: experimental
        '''
        DISK_READ_BYTES = "DISK_READ_BYTES"
        '''
        :stability: experimental
        '''
        DISK_WRITE_BYTES = "DISK_WRITE_BYTES"
        '''
        :stability: experimental
        '''
        NETWORK_IN = "NETWORK_IN"
        '''
        :stability: experimental
        '''
        NETWORK_OUT = "NETWORK_OUT"
        '''
        :stability: experimental
        '''
        NETWORK_PACKETS_IN = "NETWORK_PACKETS_IN"
        '''
        :stability: experimental
        '''
        NETWORK_PACKETS_OUT = "NETWORK_PACKETS_OUT"
        '''
        :stability: experimental
        '''
        STATUS_CHECK_FAILED = "STATUS_CHECK_FAILED"
        '''
        :stability: experimental
        '''
        STATUS_CHECK_FAILED_INSTANCE = "STATUS_CHECK_FAILED_INSTANCE"
        '''
        :stability: experimental
        '''
        STATUS_CHECK_FAILED_SYSTEM = "STATUS_CHECK_FAILED_SYSTEM"
        '''
        :stability: experimental
        '''
        METADATA_NO_TOKEN = "METADATA_NO_TOKEN"
        '''
        :stability: experimental
        '''
        CPU_CREDIT_USAGE = "CPU_CREDIT_USAGE"
        '''
        :stability: experimental
        '''
        CPU_CREDIT_BALANCE = "CPU_CREDIT_BALANCE"
        '''
        :stability: experimental
        '''
        CPU_SURPLUS_CREDIT_BALANCE = "CPU_SURPLUS_CREDIT_BALANCE"
        '''
        :stability: experimental
        '''
        CPU_SURPLUS_CREDITS_CHARGED = "CPU_SURPLUS_CREDITS_CHARGED"
        '''
        :stability: experimental
        '''


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.Ec2AutomatedShutdownProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_config": "alarmConfig",
        "encryption": "encryption",
        "lambda_configuration": "lambdaConfiguration",
    },
)
class Ec2AutomatedShutdownProps:
    def __init__(
        self,
        *,
        alarm_config: typing.Optional[typing.Union[AlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_9f8afc24, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alarm_config: (experimental) Optional custom metric configuration. If not provided, defaults to CPU utilization with a 5% threshold.
        :param encryption: (experimental) Optional KMS Encryption Key to use for encrypting resources.
        :param lambda_configuration: (experimental) Optional Lambda configuration settings.

        :stability: experimental
        '''
        if isinstance(alarm_config, dict):
            alarm_config = AlarmConfig(**alarm_config)
        if isinstance(lambda_configuration, dict):
            lambda_configuration = _LambdaConfiguration_9f8afc24(**lambda_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83540f2382d64c8555b218f2ff30272931154c2fa9cc6a7208052b6295a558dc)
            check_type(argname="argument alarm_config", value=alarm_config, expected_type=type_hints["alarm_config"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument lambda_configuration", value=lambda_configuration, expected_type=type_hints["lambda_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_config is not None:
            self._values["alarm_config"] = alarm_config
        if encryption is not None:
            self._values["encryption"] = encryption
        if lambda_configuration is not None:
            self._values["lambda_configuration"] = lambda_configuration

    @builtins.property
    def alarm_config(self) -> typing.Optional[AlarmConfig]:
        '''(experimental) Optional custom metric configuration.

        If not provided, defaults to CPU utilization with a 5% threshold.

        :stability: experimental
        '''
        result = self._values.get("alarm_config")
        return typing.cast(typing.Optional[AlarmConfig], result)

    @builtins.property
    def encryption(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Optional KMS Encryption Key to use for encrypting resources.

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def lambda_configuration(self) -> typing.Optional[_LambdaConfiguration_9f8afc24]:
        '''(experimental) Optional Lambda configuration settings.

        :stability: experimental
        '''
        result = self._values.get("lambda_configuration")
        return typing.cast(typing.Optional[_LambdaConfiguration_9f8afc24], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AutomatedShutdownProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class SecureSageMakerNotebook(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.SecureSageMakerNotebook",
):
    '''(experimental) Aspect that enforces security controls on SageMaker Notebook Instances by requiring VPC placement, disabling direct internet access, and preventing root access to the notebook environment.

    This Aspect enforces these settings through a combination of setting
    the CloudFormation properties on the Notebook resource and attaching a
    DENY policy to the role that is used by the notebook. The policy will enforce
    that the following API actions contain the correct properties to ensure
    network isolation and that the VPC subnets are set:

    - 'sagemaker:CreateTrainingJob',
    - 'sagemaker:CreateHyperParameterTuningJob',
    - 'sagemaker:CreateModel',
    - 'sagemaker:CreateProcessingJob'

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        allowed_launch_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
        notebook_subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        direct_internet_access: typing.Optional[builtins.bool] = None,
        root_access: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allowed_launch_subnets: (experimental) Sets the VPC Subnets that the SageMaker Notebook Instance is allowed to launch training and inference jobs into. This is enforced by adding DENY statements to the existing role that the Notebook Instance is using.
        :param notebook_subnet: (experimental) Sets the VPC Subnet for the Sagemaker Notebook Instance. This ensures the notebook is locked down to a specific VPC/subnet.
        :param direct_internet_access: (experimental) Sets the ``directInternetAccess`` property on the SageMaker Notebooks. By default, this is set to false to disable internet access on any SageMaker Notebook Instance that this aspect is applied to. Default: false
        :param root_access: (experimental) Sets the ``rootAccess`` property on the SageMaker Notebooks. By default, this is set to false to disable root access on any SageMaker Notebook Instance that this aspect is applied to. Default: false

        :stability: experimental
        '''
        props = SecureSageMakerNotebookProps(
            allowed_launch_subnets=allowed_launch_subnets,
            notebook_subnet=notebook_subnet,
            direct_internet_access=direct_internet_access,
            root_access=root_access,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a464b02c9d6c229339c86791c1baab1f5ba38ab5169541c238b05bf23a2fd388)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.SecureSageMakerNotebookProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_launch_subnets": "allowedLaunchSubnets",
        "notebook_subnet": "notebookSubnet",
        "direct_internet_access": "directInternetAccess",
        "root_access": "rootAccess",
    },
)
class SecureSageMakerNotebookProps:
    def __init__(
        self,
        *,
        allowed_launch_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
        notebook_subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        direct_internet_access: typing.Optional[builtins.bool] = None,
        root_access: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allowed_launch_subnets: (experimental) Sets the VPC Subnets that the SageMaker Notebook Instance is allowed to launch training and inference jobs into. This is enforced by adding DENY statements to the existing role that the Notebook Instance is using.
        :param notebook_subnet: (experimental) Sets the VPC Subnet for the Sagemaker Notebook Instance. This ensures the notebook is locked down to a specific VPC/subnet.
        :param direct_internet_access: (experimental) Sets the ``directInternetAccess`` property on the SageMaker Notebooks. By default, this is set to false to disable internet access on any SageMaker Notebook Instance that this aspect is applied to. Default: false
        :param root_access: (experimental) Sets the ``rootAccess`` property on the SageMaker Notebooks. By default, this is set to false to disable root access on any SageMaker Notebook Instance that this aspect is applied to. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0197024255c2663b7f9595b48f375b3bd3bb1aad713992f2d1205a74c784028)
            check_type(argname="argument allowed_launch_subnets", value=allowed_launch_subnets, expected_type=type_hints["allowed_launch_subnets"])
            check_type(argname="argument notebook_subnet", value=notebook_subnet, expected_type=type_hints["notebook_subnet"])
            check_type(argname="argument direct_internet_access", value=direct_internet_access, expected_type=type_hints["direct_internet_access"])
            check_type(argname="argument root_access", value=root_access, expected_type=type_hints["root_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_launch_subnets": allowed_launch_subnets,
            "notebook_subnet": notebook_subnet,
        }
        if direct_internet_access is not None:
            self._values["direct_internet_access"] = direct_internet_access
        if root_access is not None:
            self._values["root_access"] = root_access

    @builtins.property
    def allowed_launch_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) Sets the VPC Subnets that the SageMaker Notebook Instance is allowed to launch training and inference jobs into.

        This is enforced by adding
        DENY statements to the existing role that the Notebook Instance is using.

        :stability: experimental
        '''
        result = self._values.get("allowed_launch_subnets")
        assert result is not None, "Required property 'allowed_launch_subnets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], result)

    @builtins.property
    def notebook_subnet(self) -> _aws_cdk_aws_ec2_ceddda9d.ISubnet:
        '''(experimental) Sets the VPC Subnet for the Sagemaker Notebook Instance.

        This ensures the
        notebook is locked down to a specific VPC/subnet.

        :stability: experimental
        '''
        result = self._values.get("notebook_subnet")
        assert result is not None, "Required property 'notebook_subnet' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISubnet, result)

    @builtins.property
    def direct_internet_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Sets the ``directInternetAccess`` property on the SageMaker Notebooks.

        By default, this is set to false to disable internet access on any
        SageMaker Notebook Instance that this aspect is applied to.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("direct_internet_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Sets the ``rootAccess`` property on the SageMaker Notebooks.

        By default, this is set to false to disable root access on any
        SageMaker Notebook Instance that this aspect is applied to.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("root_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureSageMakerNotebookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class SetLogRetention(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.SetLogRetention",
):
    '''(experimental) Aspect that sets the log retention period for CloudWatch log groups to a user-supplied retention period.

    :stability: experimental

    Example::

        import { App, Aspects } from 'aws-cdk-lib';
        import { RetentionDays } from 'aws-cdk-lib/aws-logs';
        import { SetLogRetention } from '@cdklabs/cdk-proserve-lib/aspects';
        
        const app = new App();
        
        Aspects.of(app).add(
          new SetLogRetention({ period: RetentionDays.EIGHTEEN_MONTHS })
        );
    '''

    def __init__(self, *, period: _aws_cdk_aws_logs_ceddda9d.RetentionDays) -> None:
        '''(experimental) Creates a new instance of SetLogRetention.

        :param period: (experimental) The retention period for the logs.

        :stability: experimental
        '''
        props = SetLogRetentionProps(period=period)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visits a construct and sets log retention if applicable.

        :param node: The construct being visited.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7918d457f7130a0f58324294dfa0117ad91d007dd1efe356a28e1e7b14078104)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.SetLogRetentionProps",
    jsii_struct_bases=[],
    name_mapping={"period": "period"},
)
class SetLogRetentionProps:
    def __init__(self, *, period: _aws_cdk_aws_logs_ceddda9d.RetentionDays) -> None:
        '''(experimental) Properties for configuring log retention settings.

        :param period: (experimental) The retention period for the logs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72586255662d60e597233cf4d140d0e0bbb27e128c37bd403552be4906e4252b)
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "period": period,
        }

    @builtins.property
    def period(self) -> _aws_cdk_aws_logs_ceddda9d.RetentionDays:
        '''(experimental) The retention period for the logs.

        :stability: experimental
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.RetentionDays, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetLogRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class SqsRequireSsl(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.aspects.SqsRequireSsl",
):
    '''(experimental) Enforces SSL/TLS requirements on Simple Queue Service (SQS) for all resources that the aspect applies to.

    This is accomplished by adding a resource policy to any SQS queue that denies
    all actions when the request is not made over a secure transport.

    :stability: experimental

    Example::

        import { App, Aspects } from 'aws-cdk-lib';
        import { SqsRequireSsl } from '@cdklabs/cdk-proserve-lib/aspects';
        
        const app = new App();
        
        Aspects.of(app).add(new SqsRequireSsl());
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visits a construct and adds SSL/TLS requirement policy if it's an SQS queue.

        :param node: The construct being visited.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88c2c2ac86ce27464fcccd4cd5509db7184536f595cf22451890aac8b865258)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


__all__ = [
    "AlarmConfig",
    "ApplyRemovalPolicy",
    "ApplyRemovalPolicyProps",
    "CreateLambdaLogGroup",
    "Ec2AutomatedShutdown",
    "Ec2AutomatedShutdownProps",
    "SecureSageMakerNotebook",
    "SecureSageMakerNotebookProps",
    "SetLogRetention",
    "SetLogRetentionProps",
    "SqsRequireSsl",
]

publication.publish()

def _typecheckingstub__39e80c1625a9aebade1607b9063a75a5e101289462594aab3e82799e39c067ab(
    *,
    comparison_operator: _aws_cdk_aws_cloudwatch_ceddda9d.ComparisonOperator,
    datapoints_to_alarm: jsii.Number,
    evaluation_periods: jsii.Number,
    metric_name: Ec2AutomatedShutdown.Ec2MetricName,
    period: _aws_cdk_ceddda9d.Duration,
    statistic: builtins.str,
    threshold: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ce1ca35633c77f43304cf7f1782f1ebf1496f151645dca582fc865fe0fe866(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858f2996365d3ec27b04534ec073a42ea6b65c3aa7cc1fa650e2765c14c83528(
    *,
    removal_policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6b301934b30a296211f1f67b29307771270f03bbb136c1415e30d55396295a(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5994fe93c71f1c46730fa11383aefb416e003558c08ffb0724aa66546df71bf(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83540f2382d64c8555b218f2ff30272931154c2fa9cc6a7208052b6295a558dc(
    *,
    alarm_config: typing.Optional[typing.Union[AlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_9f8afc24, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a464b02c9d6c229339c86791c1baab1f5ba38ab5169541c238b05bf23a2fd388(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0197024255c2663b7f9595b48f375b3bd3bb1aad713992f2d1205a74c784028(
    *,
    allowed_launch_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
    notebook_subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
    direct_internet_access: typing.Optional[builtins.bool] = None,
    root_access: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7918d457f7130a0f58324294dfa0117ad91d007dd1efe356a28e1e7b14078104(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72586255662d60e597233cf4d140d0e0bbb27e128c37bd403552be4906e4252b(
    *,
    period: _aws_cdk_aws_logs_ceddda9d.RetentionDays,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88c2c2ac86ce27464fcccd4cd5509db7184536f595cf22451890aac8b865258(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
