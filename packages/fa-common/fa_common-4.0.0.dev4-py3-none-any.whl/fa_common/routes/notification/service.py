import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from fastapi import APIRouter, Depends, Header, HTTPException

from fa_common import logger
from fa_common.config import get_settings
from fa_common.routes.notification.enums import EmailBodyType
from fa_common.routes.notification.models import CallbackMetaData
from fa_common.routes.workflow import service
from fa_common.workflow.enums import JobStatus


async def send_email(to_email: str, subject: str, body: str, body_type: EmailBodyType = EmailBodyType.PLAIN):
    msg = MIMEMultipart()
    msg["From"] = get_settings().SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    if body_type == EmailBodyType.PLAIN:
        msg.attach(MIMEText(body, "plain"))
    else:
        msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(get_settings().SMTP_SERVER, get_settings().SMTP_PORT)
        server.starttls()
        server.login(get_settings().SMTP_USERNAME, get_settings().SMTP_PASSWORD)
        server.sendmail(get_settings().SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        logger.info(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"❌ Error sending email to {to_email}: {e}")


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != get_settings().MASTER_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key


def notify(router: APIRouter, path: str, subject: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)

                payload = kwargs["payload"]  # Expecting payload argument to always be present

                metadata = CallbackMetaData(**payload.get("metadata", {}))
                workflow_id = payload.get("workflow_id", None)
                if metadata.user_email is None:
                    logger.warning("⚠️ No recipient_email found in payload, skipping email.")
                    return

                if workflow_id is None:
                    logger.error("❌ Workflw id was expected in the callback but it is missing. Skipping sending an email.")
                    return

                if metadata.storage_location is None:
                    logger.error("❌ The storage location of the workflow is UNKNOWN. It was expected in the callback but it is missing!")

                workflow = await service.get_workflow(workflow_id=workflow_id, storage_location=metadata.storage_location)

                logger.info(f"Workflow successfully retrieved: {workflow.workflow_id} - {workflow.status}")

                stat_msg = f"Workflow '{workflow.workflow_id}' finshed with status of ✅ {workflow.status.value}.<br><br>"
                if workflow.status == JobStatus.FAILED:
                    stat_msg = f"Workflow '{workflow.workflow_id}' failed ❌ {workflow.status.value}.<br><br>"

                final_subject = f"{subject} - {workflow.workflow_id}"
                # if workflow.status == JobStatus.FAILED:
                #     final_subject[0] = "❌"

                summary_msg = f"""
                SUMMARY<br>
                =======<br>
                <table>
                    <tr>
                        <td>started at:</td>
                        <td>{datetime.fromisoformat(workflow.started_at).strftime("%A, %d %B %Y at %I:%M %p %Z")}</td>
                    </tr>
                    <tr>
                        <td>finished at:</td>
                        <td>{datetime.fromisoformat(workflow.finished_at).strftime("%A, %d %B %Y at %I:%M %p %Z")}</td>
                    </tr>
                    <tr>
                        <td>status:</td>
                        <td>{workflow.status.value}</td>
                    </tr>
                    <tr>
                        <td>message:</td>
                        <td>{workflow.message}</td>
                    </tr>
                </table><br><br>
                """

                link_to_res = f"""
                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td bgcolor="#0078D4" style="border-radius: 4px; padding: 10px 20px;">
                            <a href="{metadata.ui_res_link if metadata.ui_res_link else payload.get("base_url")}"
                                target="_blank"
                                style="
                                display: inline-block;
                                font-family: 'Segoe UI', sans-serif;
                                font-size: 14px;
                                color: #ffffff;
                                text-decoration: none;
                                font-weight: bold;
                                ">
                                View Results
                            </a>
                        </td>
                    </tr>
                    </table>
                    """

                # @TODO: Extract the workflow id or title, and maybe some meta info
                # such as when it started and when it finished, and specially, the status
                body_html = f"""
                <html>
                <body>
                {metadata.user_name},<br><br>

                {stat_msg}

                {summary_msg}

                {link_to_res}<br><br>

                {metadata.extra_content.body if metadata.extra_content else ""}
                </html>
                </body>
                """

                await send_email(metadata.user_email, final_subject, body_html, body_type=EmailBodyType.HTML)

                return result
            except Exception as e:
                logger.error(f"❌ An error occured during sending the email. {e!s}")

        # REGISTER CALLBACK ROUTER
        router.add_api_route(path, wrapper, methods=["POST"], dependencies=[Depends(verify_api_key)])
        return wrapper

    return decorator
