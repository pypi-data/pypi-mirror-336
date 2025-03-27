# Amazon Data Firehose Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to aws-cdk-lib/aws-kinesisfirehose.

[Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html), [formerly known as Amazon Kinesis Data Firehose](https://aws.amazon.com/about-aws/whats-new/2024/02/amazon-data-firehose-formerly-kinesis-data-firehose/),
is a service for fully-managed delivery of real-time streaming data to storage services
such as Amazon S3, Amazon Redshift, Amazon Elasticsearch, Splunk, or any custom HTTP
endpoint or third-party services such as Datadog, Dynatrace, LogicMonitor, MongoDB, New
Relic, and Sumo Logic.

Amazon Data Firehose delivery streams are distinguished from Kinesis data streams in
their models of consumption. Whereas consumers read from a data stream by actively pulling
data from the stream, a delivery stream pushes data to its destination on a regular
cadence. This means that data streams are intended to have consumers that do on-demand
processing, like AWS Lambda or Amazon EC2. On the other hand, delivery streams are
intended to have destinations that are sources for offline processing and analytics, such
as Amazon S3 and Amazon Redshift.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk)
project. It allows you to define Amazon Data Firehose delivery streams.

## Defining a Delivery Stream

In order to define a Delivery Stream, you must specify a destination. An S3 bucket can be
used as a destination. Currently the CDK supports only S3 as a destination which is covered [below](#destinations).

```python
bucket = s3.Bucket(self, "Bucket")
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destinations.S3Bucket(bucket)
)
```

The above example defines the following resources:

* An S3 bucket
* An Amazon Data Firehose delivery stream with Direct PUT as the source and CloudWatch
  error logging turned on.
* An IAM role which gives the delivery stream permission to write to the S3 bucket.

## Sources

An Amazon Data Firehose delivery stream can accept data from three main sources: Kinesis Data Streams, Managed Streaming for Apache Kafka (MSK), or via a "direct put" (API calls). Currently only Kinesis Data Streams and direct put are supported in the CDK.

See: [Sending Data to a Delivery Stream](https://docs.aws.amazon.com/firehose/latest/dev/basic-write.html)
in the *Amazon Data Firehose Developer Guide*.

### Kinesis Data Stream

A delivery stream can read directly from a Kinesis data stream as a consumer of the data
stream. Configure this behaviour by passing in a data stream in the `source`
property via the `KinesisStreamSource` class when constructing a delivery stream:

```python
# destination: firehose.IDestination

source_stream = kinesis.Stream(self, "Source Stream")

firehose.DeliveryStream(self, "Delivery Stream",
    source=firehose.KinesisStreamSource(source_stream),
    destination=destination
)
```

### Direct Put

Data must be provided via "direct put", ie., by using a `PutRecord` or
`PutRecordBatch` API call. There are a number of ways of doing so, such as:

* Kinesis Agent: a standalone Java application that monitors and delivers files while
  handling file rotation, checkpointing, and retries. See: [Writing to Amazon Data Firehose Using Kinesis Agent](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-agents.html)
  in the *Amazon Data Firehose Developer Guide*.
* AWS SDK: a general purpose solution that allows you to deliver data to a delivery stream
  from anywhere using Java, .NET, Node.js, Python, or Ruby. See: [Writing to Amazon Data Firehose Using the AWS SDK](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-sdk.html)
  in the *Amazon Data Firehose Developer Guide*.
* CloudWatch Logs: subscribe to a log group and receive filtered log events directly into
  a delivery stream. See: [logs-destinations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-logs-destinations-readme.html).
* Eventbridge: add an event rule target to send events to a delivery stream based on the
  rule filtering. See: [events-targets](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-targets-readme.html).
* SNS: add a subscription to send all notifications from the topic to a delivery
  stream. See: [sns-subscriptions](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-sns-subscriptions-readme.html).
* IoT: add an action to an IoT rule to send various IoT information to a delivery stream

## Destinations

Amazon Data Firehose supports multiple AWS and third-party services as destinations, including Amazon S3, Amazon Redshift, and more. You can find the full list of supported destination [here](https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html).

Currently in the AWS CDK, only S3 is implemented as an L2 construct destination. Other destinations can still be configured using L1 constructs. See [kinesisfirehose-destinations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-kinesisfirehose-destinations-readme.html)
for the implementations of these destinations.

### S3

Defining a delivery stream with an S3 bucket destination:

```python
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket)

firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

The S3 destination also supports custom dynamic prefixes. `dataOutputPrefix`
will be used for files successfully delivered to S3. `errorOutputPrefix` will be added to
failed records before writing them to S3.

```python
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket,
    data_output_prefix="myFirehose/DeliveredYear=!{timestamp:yyyy}/anyMonth/rand=!{firehose:random-string}",
    error_output_prefix="myFirehoseFailures/!{firehose:error-output-type}/!{timestamp:yyyy}/anyMonth/!{timestamp:dd}"
)
```

See: [Custom S3 Prefixes](https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html)
in the *Amazon Data Firehose Developer Guide*.

## Server-side Encryption

Enabling server-side encryption (SSE) requires Amazon Data Firehose to encrypt all data
sent to delivery stream when it is stored at rest. This means that data is encrypted
before being written to the service's internal storage layer and decrypted after it is
received from the internal storage layer. The service manages keys and cryptographic
operations so that sources and destinations do not need to, as the data is encrypted and
decrypted at the boundaries of the service (i.e., before the data is delivered to a
destination). By default, delivery streams do not have SSE enabled.

The Key Management Service keys (KMS keys) used for SSE can either be AWS-owned or
customer-managed. AWS-owned KMS keys are created, owned and managed by AWS for use in
multiple AWS accounts. As a customer, you cannot view, use, track, or manage these keys,
and you are not charged for their use. On the other hand, customer-managed KMS keys are
created and owned within your account and managed entirely by you. As a customer, you are
responsible for managing access, rotation, aliases, and deletion for these keys, and you
are changed for their use.

See: [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys)
in the *KMS Developer Guide*.

```python
# destination: firehose.IDestination
# SSE with an customer-managed key that is explicitly specified
# key: kms.Key


# SSE with an AWS-owned key
firehose.DeliveryStream(self, "Delivery Stream with AWS Owned Key",
    encryption=firehose.StreamEncryption.aws_owned_key(),
    destination=destination
)
# SSE with an customer-managed key that is created automatically by the CDK
firehose.DeliveryStream(self, "Delivery Stream with Customer Managed Key",
    encryption=firehose.StreamEncryption.customer_managed_key(),
    destination=destination
)
firehose.DeliveryStream(self, "Delivery Stream with Customer Managed and Provided Key",
    encryption=firehose.StreamEncryption.customer_managed_key(key),
    destination=destination
)
```

See: [Data Protection](https://docs.aws.amazon.com/firehose/latest/dev/encryption.html)
in the *Amazon Data Firehose Developer Guide*.

## Monitoring

Amazon Data Firehose is integrated with CloudWatch, so you can monitor the performance of
your delivery streams via logs and metrics.

### Logs

Amazon Data Firehose will send logs to CloudWatch when data transformation or data
delivery fails. The CDK will enable logging by default and create a CloudWatch LogGroup
and LogStream with default settings for your Delivery Stream.

When creating a destination, you can provide an `ILoggingConfig`, which can either be an `EnableLogging` or `DisableLogging` instance.
If you use `EnableLogging`, the CDK will create a CloudWatch LogGroup and LogStream with all CloudFormation default settings for you, or you can optionally
specify your own log group to be used for capturing and storing log events. For example:

```python
import aws_cdk.aws_logs as logs
# bucket: s3.Bucket


log_group = logs.LogGroup(self, "Log Group")
destination = destinations.S3Bucket(bucket,
    logging_config=destinations.EnableLogging(log_group)
)

firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

Logging can also be disabled:

```python
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    logging_config=destinations.DisableLogging()
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

See: [Monitoring using CloudWatch Logs](https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-logs.html)
in the *Amazon Data Firehose Developer Guide*.

### Metrics

Amazon Data Firehose sends metrics to CloudWatch so that you can collect and analyze the
performance of the delivery stream, including data delivery, data ingestion, data
transformation, format conversion, API usage, encryption, and resource usage. You can then
use CloudWatch alarms to alert you, for example, when data freshness (the age of the
oldest record in the delivery stream) exceeds the buffering limit (indicating that data is
not being delivered to your destination), or when the rate of incoming records exceeds the
limit of records per second (indicating data is flowing into your delivery stream faster
than it is configured to process).

CDK provides methods for accessing delivery stream metrics with default configuration,
such as `metricIncomingBytes`, and `metricIncomingRecords` (see [`IDeliveryStream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.IDeliveryStream.html)
for a full list). CDK also provides a generic `metric` method that can be used to produce
metric configurations for any metric provided by Amazon Data Firehose; the configurations
are pre-populated with the correct dimensions for the delivery stream.

```python
import aws_cdk.aws_cloudwatch as cloudwatch

# delivery_stream: firehose.DeliveryStream


# Alarm that triggers when the per-second average of incoming bytes exceeds 90% of the current service limit
incoming_bytes_percent_of_limit = cloudwatch.MathExpression(
    expression="incomingBytes / 300 / bytePerSecLimit",
    using_metrics={
        "incoming_bytes": delivery_stream.metric_incoming_bytes(statistic=cloudwatch.Statistic.SUM),
        "byte_per_sec_limit": delivery_stream.metric("BytesPerSecondLimit")
    }
)

cloudwatch.Alarm(self, "Alarm",
    metric=incoming_bytes_percent_of_limit,
    threshold=0.9,
    evaluation_periods=3
)
```

See: [Monitoring Using CloudWatch Metrics](https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-metrics.html)
in the *Amazon Data Firehose Developer Guide*.

## Compression

Your data can automatically be compressed when it is delivered to S3 as either a final or
an intermediary/backup destination. Supported compression formats are: gzip, Snappy,
Hadoop-compatible Snappy, and ZIP, except for Redshift destinations, where Snappy
(regardless of Hadoop-compatibility) and ZIP are not supported. By default, data is
delivered to S3 without compression.

```python
# Compress data delivered to S3 using Snappy
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket,
    compression=destinations.Compression.SNAPPY
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

## Buffering

Incoming data is buffered before it is delivered to the specified destination. The
delivery stream will wait until the amount of incoming data has exceeded some threshold
(the "buffer size") or until the time since the last data delivery occurred exceeds some
threshold (the "buffer interval"), whichever happens first. You can configure these
thresholds based on the capabilities of the destination and your use-case. By default, the
buffer size is 5 MiB and the buffer interval is 5 minutes.

```python
# Increase the buffer interval and size to 10 minutes and 8 MiB, respectively
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    buffering_interval=Duration.minutes(10),
    buffering_size=Size.mebibytes(8)
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

See: [Data Delivery Frequency](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#frequency)
in the *Amazon Data Firehose Developer Guide*.

Zero buffering, where Amazon Data Firehose stream can be configured to not buffer data before delivery, is supported by
setting the "buffer interval" to 0.

```python
# Setup zero buffering
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    buffering_interval=Duration.seconds(0)
)
firehose.DeliveryStream(self, "ZeroBufferDeliveryStream",
    destination=destination
)
```

See: [Buffering Hints](https://docs.aws.amazon.com/firehose/latest/dev/buffering-hints.html).

## Destination Encryption

Your data can be automatically encrypted when it is delivered to S3 as a final or an
intermediary/backup destination. Amazon Data Firehose supports Amazon S3 server-side
encryption with AWS Key Management Service (AWS KMS) for encrypting delivered data in
Amazon S3. You can choose to not encrypt the data or to encrypt with a key from the list
of AWS KMS keys that you own. For more information,
see [Protecting Data Using Server-Side Encryption with AWS KMS–Managed Keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html).
By default, encryption isn’t directly enabled on the delivery stream; instead, it uses the default encryption settings of the destination S3 bucket.

```python
# bucket: s3.Bucket
# key: kms.Key

destination = destinations.S3Bucket(bucket,
    encryption_key=key
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

## Backup

A delivery stream can be configured to back up data to S3 that it attempted to deliver to
the configured destination. Backed up data can be all the data that the delivery stream
attempted to deliver or just data that it failed to deliver (Redshift and S3 destinations
can only back up all data). CDK can create a new S3 bucket where it will back up data, or
you can provide a bucket where data will be backed up. You can also provide a prefix under
which your backed-up data will be placed within the bucket. By default, source data is not
backed up to S3.

```python
# Enable backup of all source records (to an S3 bucket created by CDK).
# bucket: s3.Bucket
# Explicitly provide an S3 bucket to which all source records will be backed up.
# backup_bucket: s3.Bucket

firehose.DeliveryStream(self, "Delivery Stream Backup All",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL
        )
    )
)
firehose.DeliveryStream(self, "Delivery Stream Backup All Explicit Bucket",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            bucket=backup_bucket
        )
    )
)
# Explicitly provide an S3 prefix under which all source records will be backed up.
firehose.DeliveryStream(self, "Delivery Stream Backup All Explicit Prefix",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL,
            data_output_prefix="mybackup"
        )
    )
)
```

If any Data Processing or Transformation is configured on your Delivery Stream, the source
records will be backed up in their original format.

## Data Processing/Transformation

Data can be transformed before being delivered to destinations. There are two types of
data processing for delivery streams: record transformation with AWS Lambda, and record
format conversion using a schema stored in an AWS Glue table. If both types of data
processing are configured, then the Lambda transformation is performed first. By default,
no data processing occurs. This construct library currently only supports data
transformation with AWS Lambda. See [#15501](https://github.com/aws/aws-cdk/issues/15501)
to track the status of adding support for record format conversion.

### Data transformation with AWS Lambda

To transform the data, Amazon Data Firehose will call a Lambda function that you provide
and deliver the data returned in place of the source record. The function must return a
result that contains records in a specific format, including the following fields:

* `recordId` -- the ID of the input record that corresponds the results.
* `result` -- the status of the transformation of the record: "Ok" (success), "Dropped"
  (not processed intentionally), or "ProcessingFailed" (not processed due to an error).
* `data` -- the transformed data, Base64-encoded.

The data is buffered up to 1 minute and up to 3 MiB by default before being sent to the
function, but can be configured using `bufferInterval` and `bufferSize`
in the processor configuration (see: [Buffering](#buffering)). If the function invocation
fails due to a network timeout or because of hitting an invocation limit, the invocation
is retried 3 times by default, but can be configured using `retries` in the processor
configuration.

```python
# bucket: s3.Bucket
# Provide a Lambda function that will transform records before delivery, with custom
# buffering and retry configuration
lambda_function = lambda_.Function(self, "Processor",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
)
lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
    buffer_interval=Duration.minutes(5),
    buffer_size=Size.mebibytes(5),
    retries=5
)
s3_destination = destinations.S3Bucket(bucket,
    processor=lambda_processor
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

```python
import path as path
import aws_cdk.aws_kinesisfirehose_alpha as firehose
import aws_cdk.aws_kms as kms
import aws_cdk.aws_lambda_nodejs as lambdanodejs
import aws_cdk.aws_logs as logs
import aws_cdk.aws_s3 as s3
import aws_cdk as cdk
import aws_cdk.aws_kinesisfirehose_destinations_alpha as destinations
from aws_cdk.integ_tests_alpha import AwsApiCall, ExpectedResult, IntegTest

app = cdk.App()

stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")

bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBucket",
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True
)

backup_bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBackupBucket",
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True
)
log_group = logs.LogGroup(stack, "LogGroup",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
    entry=path.join(__dirname, "lambda-data-processor.js"),
    timeout=cdk.Duration.minutes(1)
)

processor = firehose.LambdaFunctionProcessor(data_processor_function,
    buffer_interval=cdk.Duration.seconds(60),
    buffer_size=cdk.Size.mebibytes(1),
    retries=1
)

key = kms.Key(stack, "Key",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

backup_key = kms.Key(stack, "BackupKey",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

delivery_stream = firehose.DeliveryStream(stack, "DeliveryStream",
    destination=destinations.S3Bucket(bucket,
        logging_config=destinations.EnableLogging(log_group),
        processor=processor,
        compression=destinations.Compression.GZIP,
        data_output_prefix="regularPrefix",
        error_output_prefix="errorPrefix",
        buffering_interval=cdk.Duration.seconds(60),
        buffering_size=cdk.Size.mebibytes(1),
        encryption_key=key,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL,
            bucket=backup_bucket,
            compression=destinations.Compression.ZIP,
            data_output_prefix="backupPrefix",
            error_output_prefix="backupErrorPrefix",
            buffering_interval=cdk.Duration.seconds(60),
            buffering_size=cdk.Size.mebibytes(1),
            encryption_key=backup_key
        )
    )
)

firehose.DeliveryStream(stack, "ZeroBufferingDeliveryStream",
    destination=destinations.S3Bucket(bucket,
        compression=destinations.Compression.GZIP,
        data_output_prefix="regularPrefix",
        error_output_prefix="errorPrefix",
        buffering_interval=cdk.Duration.seconds(0)
    )
)

test_case = IntegTest(app, "integ-tests",
    test_cases=[stack],
    regions=["us-east-1"]
)

test_case.assertions.aws_api_call("Firehose", "putRecord", {
    "DeliveryStreamName": delivery_stream.delivery_stream_name,
    "Record": {
        "Data": "testData123"
    }
})

s3_api_call = test_case.assertions.aws_api_call("S3", "listObjectsV2", {
    "Bucket": bucket.bucket_name,
    "MaxKeys": 1
}).expect(ExpectedResult.object_like({
    "KeyCount": 1
})).wait_for_assertions(
    interval=cdk.Duration.seconds(30),
    total_timeout=cdk.Duration.minutes(10)
)

if s3_api_call instanceof AwsApiCall && s3_api_call.waiter_provider:
    s3_api_call.waiter_provider.add_to_role_policy({
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": ["*"]
    })
```

See: [Data Transformation](https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html)
in the *Amazon Data Firehose Developer Guide*.

## Specifying an IAM role

The DeliveryStream class automatically creates IAM service roles with all the minimum
necessary permissions for Amazon Data Firehose to access the resources referenced by your
delivery stream. One service role is created for the delivery stream that allows Amazon
Data Firehose to read from a Kinesis data stream (if one is configured as the delivery
stream source) and for server-side encryption. Note that if the DeliveryStream is created
without specifying a `source` or `encryptionKey`, this role is not created as it is not needed.

Another service role is created for each destination, which gives Amazon Data Firehose write
access to the destination resource, as well as the ability to invoke data transformers and
read schemas for record format conversion. If you wish, you may specify your own IAM role for
either the delivery stream or the destination service role, or both. It must have the correct
trust policy (it must allow Amazon Data Firehose to assume it) or delivery stream creation or
data delivery will fail. Other required permissions to destination resources, encryption keys, etc.,
will be provided automatically.

```python
# Specify the roles created above when defining the destination and delivery stream.
# bucket: s3.Bucket
# Create service roles for the delivery stream and destination.
# These can be used for other purposes and granted access to different resources.
# They must include the Amazon Data Firehose service principal in their trust policies.
# Two separate roles are shown below, but the same role can be used for both purposes.
delivery_stream_role = iam.Role(self, "Delivery Stream Role",
    assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
)
destination_role = iam.Role(self, "Destination Role",
    assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
)
destination = destinations.S3Bucket(bucket, role=destination_role)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination,
    role=delivery_stream_role
)
```

See [Controlling Access](https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html)
in the *Amazon Data Firehose Developer Guide*.

## Granting application access to a delivery stream

IAM roles, users or groups which need to be able to work with delivery streams should be
granted IAM permissions.

Any object that implements the `IGrantable` interface (i.e., has an associated principal)
can be granted permissions to a delivery stream by calling:

* `grantPutRecords(principal)` - grants the principal the ability to put records onto the
  delivery stream
* `grant(principal, ...actions)` - grants the principal permission to a custom set of
  actions

```python
# Give the role permissions to write data to the delivery stream
# delivery_stream: firehose.DeliveryStream
lambda_role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)
delivery_stream.grant_put_records(lambda_role)
```

The following write permissions are provided to a service principal by the
`grantPutRecords()` method:

* `firehose:PutRecord`
* `firehose:PutRecordBatch`

## Granting a delivery stream access to a resource

Conversely to the above, Amazon Data Firehose requires permissions in order for delivery
streams to interact with resources that you own. For example, if an S3 bucket is specified
as a destination of a delivery stream, the delivery stream must be granted permissions to
put and get objects from the bucket. When using the built-in AWS service destinations
found in the `@aws-cdk/aws-kinesisfirehose-destinations-alpha` module, the CDK grants the
permissions automatically. However, custom or third-party destinations may require custom
permissions. In this case, use the delivery stream as an `IGrantable`, as follows:

```python
# delivery_stream: firehose.DeliveryStream
fn = lambda_.Function(self, "Function",
    code=lambda_.Code.from_inline("exports.handler = (event) => {}"),
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler"
)
fn.grant_invoke(delivery_stream)
```
