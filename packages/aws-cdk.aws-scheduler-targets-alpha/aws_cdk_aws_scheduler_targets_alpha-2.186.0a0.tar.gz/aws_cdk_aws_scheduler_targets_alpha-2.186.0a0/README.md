# Amazon EventBridge Scheduler Targets Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to `aws-cdk-lib/aws-scheduler-targets`.

[Amazon EventBridge Scheduler](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/) is a feature from Amazon EventBridge
that allows you to create, run, and manage scheduled tasks at scale. With EventBridge Scheduler, you can schedule millions of one-time or recurring tasks across various AWS services without provisioning or managing underlying infrastructure.

This library contains integration classes for Amazon EventBridge Scheduler to call any
number of supported AWS Services.

The following targets are supported:

1. `targets.LambdaInvoke`: [Invoke an AWS Lambda function](#invoke-a-lambda-function)
2. `targets.StepFunctionsStartExecution`: [Start an AWS Step Function](#start-an-aws-step-function)
3. `targets.CodeBuildStartBuild`: [Start a CodeBuild job](#start-a-codebuild-job)
4. `targets.SqsSendMessage`: [Send a Message to an Amazon SQS Queue](#send-a-message-to-an-sqs-queue)
5. `targets.SnsPublish`: [Publish messages to an Amazon SNS topic](#publish-messages-to-an-amazon-sns-topic)
6. `targets.EventBridgePutEvents`: [Put Events on EventBridge](#send-events-to-an-eventbridge-event-bus)
7. `targets.InspectorStartAssessmentRun`: [Start an Amazon Inspector assessment run](#start-an-amazon-inspector-assessment-run)
8. `targets.KinesisStreamPutRecord`: [Put a record to an Amazon Kinesis Data Stream](#put-a-record-to-an-amazon-kinesis-data-stream)
9. `targets.FirehosePutRecord`: [Put a record to an Amazon Data Firehose](#put-a-record-to-an-amazon-data-firehose)
10. `targets.CodePipelineStartPipelineExecution`: [Start a CodePipeline execution](#start-a-codepipeline-execution)
11. `targets.SageMakerStartPipelineExecution`: [Start a SageMaker pipeline execution](#start-a-sagemaker-pipeline-execution)
12. `targets.EcsRunTask`: [Start a new ECS task](#schedule-an-ecs-task-run)
13. `targets.Universal`: [Invoke a wider set of AWS API](#invoke-a-wider-set-of-aws-api)

## Invoke a Lambda function

Use the `LambdaInvoke` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
called every hour by EventBridge Scheduler with a custom payload. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
import aws_cdk.aws_lambda as lambda_


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("exports.handler = handler.toString()")
)

dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Start an AWS Step Function

Use the `StepFunctionsStartExecution` target to start a new execution on a StepFunction.

The code snippet below creates an event rule with a Step Function as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks


payload = {
    "Name": "MyParameter",
    "Value": "🌥️"
}

put_parameter_step = tasks.CallAwsService(self, "PutParameter",
    service="ssm",
    action="putParameter",
    iam_resources=["*"],
    parameters={
        "Name.$": "$.Name",
        "Value.$": "$.Value",
        "Type": "String",
        "Overwrite": True
    }
)

state_machine = sfn.StateMachine(self, "StateMachine",
    definition_body=sfn.DefinitionBody.from_chainable(put_parameter_step)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.StepFunctionsStartExecution(state_machine,
        input=ScheduleTargetInput.from_object(payload)
    )
)
```

## Start a CodeBuild job

Use the `CodeBuildStartBuild` target to start a new build run on a CodeBuild project.

The code snippet below creates an event rule with a CodeBuild project as target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codebuild as codebuild

# project: codebuild.Project


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodeBuildStartBuild(project)
)
```

## Send a Message To an SQS Queue

Use the `SqsSendMessage` target to send a message to an SQS Queue.

The code snippet below creates an event rule with an SQS Queue as a target
called every hour by EventBridge Scheduler with a custom payload.

Contains the `messageGroupId` to use when the target is a FIFO queue. If you specify
a FIFO queue as a target, the queue must have content-based deduplication enabled.

```python
payload = "test"
message_group_id = "id"
queue = sqs.Queue(self, "MyQueue",
    fifo=True,
    content_based_deduplication=True
)

target = targets.SqsSendMessage(queue,
    input=ScheduleTargetInput.from_text(payload),
    message_group_id=message_group_id
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(1)),
    target=target
)
```

## Publish messages to an Amazon SNS topic

Use the `SnsPublish` target to publish messages to an Amazon SNS topic.

The code snippets below create an event rule with a Amazon SNS topic as a target.
It's called every hour by Amazon EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_sns as sns


topic = sns.Topic(self, "Topic")

payload = {
    "message": "Hello scheduler!"
}

target = targets.SnsPublish(topic,
    input=ScheduleTargetInput.from_object(payload)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Send events to an EventBridge event bus

Use the `EventBridgePutEvents` target to send events to an EventBridge event bus.

The code snippet below creates an event rule with an EventBridge event bus as a target
called every hour by EventBridge Scheduler with a custom event payload.

```python
import aws_cdk.aws_events as events


event_bus = events.EventBus(self, "EventBus",
    event_bus_name="DomainEvents"
)

event_entry = targets.EventBridgePutEventsEntry(
    event_bus=event_bus,
    source="PetService",
    detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
    detail_type="🐶"
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.EventBridgePutEvents(event_entry)
)
```

## Start an Amazon Inspector assessment run

Use the `InspectorStartAssessmentRun` target to start an Inspector assessment run.

The code snippet below creates an event rule with an assessment template as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_inspector as inspector

# cfn_assessment_template: inspector.CfnAssessmentTemplate


assessment_template = inspector.AssessmentTemplate.from_cfn_assessment_template(self, "MyAssessmentTemplate", cfn_assessment_template)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.InspectorStartAssessmentRun(assessment_template)
)
```

## Put a record to an Amazon Kinesis Data Stream

Use the `KinesisStreamPutRecord` target to put a record to an Amazon Kinesis Data Stream.

The code snippet below creates an event rule with a stream as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_kinesis as kinesis


stream = kinesis.Stream(self, "MyStream")

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.KinesisStreamPutRecord(stream,
        partition_key="key"
    )
)
```

## Put a record to an Amazon Data Firehose

Use the `FirehosePutRecord` target to put a record to an Amazon Data Firehose delivery stream.

The code snippet below creates an event rule with a delivery stream as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_kinesisfirehose as firehose
# delivery_stream: firehose.IDeliveryStream


payload = {
    "Data": "record"
}

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.FirehosePutRecord(delivery_stream,
        input=ScheduleTargetInput.from_object(payload)
    )
)
```

## Start a CodePipeline execution

Use the `CodePipelineStartPipelineExecution` target to start a new execution for a CodePipeline pipeline.

The code snippet below creates an event rule with a CodePipeline pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codepipeline as codepipeline

# pipeline: codepipeline.Pipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodePipelineStartPipelineExecution(pipeline)
)
```

## Start a SageMaker pipeline execution

Use the `SageMakerStartPipelineExecution` target to start a new execution for a SageMaker pipeline.

The code snippet below creates an event rule with a SageMaker pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_sagemaker as sagemaker

# pipeline: sagemaker.IPipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.SageMakerStartPipelineExecution(pipeline,
        pipeline_parameter_list=[targets.SageMakerPipelineParameter(
            name="parameter-name",
            value="parameter-value"
        )]
    )
)
```

## Schedule an ECS task run

Use the `EcsRunTask` target to schedule an ECS task run for a cluster.

The code snippet below creates an event rule with a Fargate task definition and cluster as the target which is called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_ecs as ecs

# cluster: ecs.ICluster
# task_definition: ecs.FargateTaskDefinition


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
    target=targets.EcsRunFargateTask(cluster,
        task_definition=task_definition
    )
)
```

The code snippet below creates an event rule with a EC2 task definition and cluster as the target which is called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_ecs as ecs

# cluster: ecs.ICluster
# task_definition: ecs.Ec2TaskDefinition


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
    target=targets.EcsRunEc2Task(cluster,
        task_definition=task_definition
    )
)
```

## Invoke a wider set of AWS API

Use the `Universal` target to invoke AWS API. See [https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html)

The code snippet below creates an event rule with AWS API as the target which is
called at midnight every day by EventBridge Scheduler.

```python
Schedule(self, "Schedule",
    schedule=ScheduleExpression.cron(
        minute="0",
        hour="0"
    ),
    target=targets.Universal(
        service="rds",
        action="stopDBCluster",
        input=ScheduleTargetInput.from_object({
            "DbClusterIdentifier": "my-db"
        })
    )
)
```

The `service` must be in lowercase and the `action` must be in camelCase.

By default, an IAM policy for the Scheduler is extracted from the API call. The action in the policy is constructed using the `service` and `action` prop.
Re-using the example above, the action will be `rds:stopDBCluster`. Note that not all IAM actions follow the same pattern. In such scenario, please use the
`policyStatements` prop to override the policy:

```python
Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.Universal(
        service="sqs",
        action="sendMessage",
        policy_statements=[
            iam.PolicyStatement(
                actions=["sqs:SendMessage"],
                resources=["arn:aws:sqs:us-east-1:123456789012:my_queue"]
            ),
            iam.PolicyStatement(
                actions=["kms:Decrypt", "kms:GenerateDataKey*"],
                resources=["arn:aws:kms:us-east-1:123456789012:key/0987dcba-09fe-87dc-65ba-ab0987654321"]
            )
        ]
    )
)
```

> Note: The default policy uses `*` in the resources field as CDK does not have a straight forward way to auto-discover the resources permission required.
> It is recommended that you scope the field down to specific resources to have a better security posture.
