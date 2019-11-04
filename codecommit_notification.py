import os
import boto3
import push_slack

lambda_client = None
codecommit_client = None


def lambda_handler(event, context):
    global lambda_client
    if not lambda_client:
        lambda_client = boto3.client('lambda')

    notification_body = event['detail']['notificationBody']

    if event['detail-type'] == "CodeCommit Pull Request State Change":
        repository_name = event['detail']['repositoryNames'][0]
        text = ""
        if event['detail']['event'] == "pullRequestCreated":
            # プルリクエスト作成
            mention_members = os.environ.get("SLACK_MENTION_MEMBERS", "")
            mention = " ".join(
                ["<@" + u + ">" for u in mention_members.split(",")])
            message = "{} {}がプルリクエストを作成しました".format(
                mention, event['detail']['callerUserArn'].split("/")[1])
            color = "#439FE0"
            if "description" in event['detail']:
                text = "```{}```".format(event['detail']['description'])
        elif event['detail']['pullRequestStatus'] == "Closed":
            if event['detail']['isMerged'] == "False":
                # プルリクエストクローズ（CodeCommitとしてのマージではない終了）
                message = "{}がプルリクエストをクローズしました".format(
                    event['detail']['callerUserArn'].split("/")[1])
                color = "#439FE0"
            else:
                # プルリクエストがマージされた
                message = "{}がプルリクエストをマージしました".format(
                    event['detail']['callerUserArn'].split("/")[1])
                color = "good"
        else:
            # プルリクエスト更新
            message = "{}がプルリクエストを更新しました".format(
                event['detail']['callerUserArn'].split("/")[1])
            color = "#439FE0"
        title = "[{}] {}".format(repository_name, event['detail']['title'])
        pos = notification_body.find("https://")
        if pos >= 0:
            title_link = notification_body[pos:]
        else:
            title_link = ""
    elif event['detail-type'] == "CodeCommit Comment on Pull Request":
        # プルリクエストへのコメント
        repository_name = event['detail']['repositoryName']
        request_id = event['detail']['pullRequestId']
        request_title = get_pull_request_title(request_id)
        file_name, content = get_pull_request_comment_info(
            request_id, event['detail']['commentId'])
        message = "{}がプルリクエストにコメントしました".format(
            event['detail']['callerUserArn'].split("/")[1])
        title = "[{}] {}".format(repository_name, request_title)
        pos = notification_body.find("https://")
        if pos >= 0:
            title_link = notification_body[pos:]
        else:
            title_link = ""
        color = "#439FE0"
        text = "{}\n```{}```".format(file_name, content)
    elif event['detail-type'] == "CodeCommit Comment on Commit":
        # コミットへのコメント
        repository_name = event['detail']['repositoryName']
        message = "{}がコミットにコメントしました".format(
            event['detail']['callerUserArn'].split("/")[1])
        title = "[{}] {}".format(repository_name,
                                 event['detail']['afterCommitId'])
        pos = notification_body.find("https://")
        if pos >= 0:
            title_link = notification_body[pos:]
        else:
            title_link = ""
        color = "#439FE0"
        text = "```{}```".format(
            get_comment_content(event['detail']['commentId']))

    attachments_json = {
        "pretext": message,
        "title": title,
        "title_link": title_link,
        "color": color,
        "text": text
    }
    push_slack.send_to_slack(**attachments_json)


def get_pull_request_title(request_id):
    global codecommit_client
    if not codecommit_client:
        codecommit_client = boto3.client('codecommit')
    return codecommit_client.get_pull_request(
        pullRequestId=request_id)['pullRequest']['title']


def get_comment_content(comment_id):
    global codecommit_client
    if not codecommit_client:
        codecommit_client = boto3.client('codecommit')
    return codecommit_client.get_comment(
        commentId=comment_id)['comment']['content']


def get_pull_request_comment_info(request_id, comment_id):
    global codecommit_client
    if not codecommit_client:
        codecommit_client = boto3.client('codecommit')
    requests_json = codecommit_client.get_comments_for_pull_request(
        pullRequestId=request_id)
    for req in requests_json['commentsForPullRequestData']:
        for comment in req['comments']:
            if comment['commentId'] == comment_id:
                if 'location' in req:
                    return (req['location']['filePath'], comment['content'])
                else:
                    return ("", comment['content'])
