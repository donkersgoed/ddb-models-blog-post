import aws_cdk as core
import aws_cdk.assertions as assertions

from ddb_models_blog_post.ddb_models_blog_post_stack import DdbModelsBlogPostStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ddb_models_blog_post/ddb_models_blog_post_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DdbModelsBlogPostStack(app, "ddb-models-blog-post")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
