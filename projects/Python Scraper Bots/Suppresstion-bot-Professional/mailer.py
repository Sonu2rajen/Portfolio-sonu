"""
Email Module
Sends suppression alert emails with HTML formatting and Excel attachment.
"""

import smtplib
import ssl
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

logger = logging.getLogger(__name__)


# =========================================================
# BUILD HTML EMAIL
# =========================================================

def build_html_email(df_new_suppressions, summary, brand="Clicktech"):
    """Build a professional HTML email body."""

    today = datetime.now().strftime("%d %B %Y")
    new_count = len(df_new_suppressions)

    # Color theme
    header_bg = "#1F4E79"
    accent = "#2E86AB"

    warning_bg = (
        "#FFF3CD"
        if new_count > 0
        else "#D4EDDA"
    )

    warning_border = (
        "#FFC107"
        if new_count > 0
        else "#28A745"
    )

    warning_icon = (
        "⚠️"
        if new_count > 0
        else "✅"
    )

    # -----------------------------------------------------
    # ASIN TABLE
    # -----------------------------------------------------

    if new_count > 0:

        asin_rows = ""

        for i, (_, row) in enumerate(
            df_new_suppressions.iterrows()
        ):

            bg = (
                "#FFFFFF"
                if i % 2 == 0
                else "#F8F9FA"
            )

            asin_rows += f"""
            <tr style="background:{bg}">
                <td style="
                    padding:10px 15px;
                    border-bottom:1px solid #DEE2E6;
                    font-weight:bold;
                    color:#1F4E79
                ">
                    {row['ASIN']}
                </td>

                <td style="
                    padding:10px 15px;
                    border-bottom:1px solid #DEE2E6;
                    color:#DC3545
                ">
                    {row.get('Availability', 'N/A')}
                </td>

                <td style="
                    padding:10px 15px;
                    border-bottom:1px solid #DEE2E6
                ">
                    {row.get('Asin Search', 'N/A')}
                </td>

                <td style="
                    padding:10px 15px;
                    border-bottom:1px solid #DEE2E6
                ">
                    {row.get('Asin Refelct', 'N/A')}
                </td>

                <td style="
                    padding:10px 15px;
                    border-bottom:1px solid #DEE2E6;
                    font-weight:bold;
                    color:#28A745
                ">
                    {int(row.get('sellable', 0))}
                </td>
            </tr>
            """

        asin_table = f"""
        <h3 style="
            color:{header_bg};
            margin-top:30px;
        ">
            🔴 Newly Suppressed ASINs ({new_count})
        </h3>

        <table style="
            width:100%;
            border-collapse:collapse;
            border-radius:8px;
            overflow:hidden;
            box-shadow:0 2px 8px rgba(0,0,0,0.1)
        ">

            <thead>
                <tr style="background:{header_bg}">
                    <th style="
                        padding:12px 15px;
                        color:#fff;
                        text-align:left
                    ">
                        ASIN
                    </th>

                    <th style="
                        padding:12px 15px;
                        color:#fff;
                        text-align:left
                    ">
                        Availability
                    </th>

                    <th style="
                        padding:12px 15px;
                        color:#fff;
                        text-align:left
                    ">
                        ASIN Search
                    </th>

                    <th style="
                        padding:12px 15px;
                        color:#fff;
                        text-align:left
                    ">
                        ASIN Reflect
                    </th>

                    <th style="
                        padding:12px 15px;
                        color:#fff;
                        text-align:left
                    ">
                        Sellable Qty
                    </th>
                </tr>
            </thead>

            <tbody>
                {asin_rows}
            </tbody>

        </table>
        """

    else:

        asin_table = """
        <div style="
            background:#D4EDDA;
            border:1px solid #C3E6CB;
            border-radius:8px;
            padding:20px;
            text-align:center;
            margin-top:20px
        ">

            <h3 style="
                color:#155724;
                margin:0
            ">
                ✅ No New Suppressions Found Today
            </h3>

            <p style="
                color:#155724;
                margin:5px 0 0 0
            ">
                All ASINs are healthy and accounted for.
            </p>

        </div>
        """

    # -----------------------------------------------------
    # COMPLETE HTML EMAIL
    # -----------------------------------------------------

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>
        <meta charset="UTF-8">
    </head>

    <body style="
        margin:0;
        padding:0;
        font-family:'Segoe UI',Arial,sans-serif;
        background:#F0F4F8
    ">

        <table
            width="100%"
            cellpadding="0"
            cellspacing="0"
            style="
                background:#F0F4F8;
                padding:30px 0
            "
        >

            <tr>

                <td align="center">

                    <table
                        width="700"
                        cellpadding="0"
                        cellspacing="0"
                        style="
                            background:#FFFFFF;
                            border-radius:12px;
                            overflow:hidden;
                            box-shadow:0 4px 20px rgba(0,0,0,0.15)
                        "
                    >

                        <!-- HEADER -->

                        <tr>

                            <td style="
                                background:{header_bg};
                                padding:30px 40px;
                                text-align:center
                            ">

                                <h1 style="
                                    color:#FFFFFF;
                                    margin:0;
                                    font-size:24px;
                                    letter-spacing:1px
                                ">
                                    📦 {brand} Suppression Report
                                </h1>

                                <p style="
                                    color:#BDD5EA;
                                    margin:8px 0 0 0;
                                    font-size:14px
                                ">
                                    {today} |
                                    Auto-generated by Suppression Monitor
                                </p>

                            </td>

                        </tr>


                        <!-- ALERT BANNER -->

                        <tr>

                            <td style="
                                padding:20px 40px 0 40px
                            ">

                                <div style="
                                    background:{warning_bg};
                                    border-left:5px solid {warning_border};
                                    border-radius:4px;
                                    padding:15px 20px
                                ">

                                    <strong style="font-size:16px">

                                        {warning_icon}
                                        {new_count}
                                        New Suppression(s)
                                        Detected Today

                                    </strong>

                                </div>

                            </td>

                        </tr>


                        <!-- SUMMARY -->

                        <tr>

                            <td style="
                                padding:25px 40px 0 40px
                            ">

                                <h3 style="
                                    color:{header_bg};
                                    margin:0 0 15px 0;
                                    border-bottom:2px solid {accent};
                                    padding-bottom:8px
                                ">
                                    📊 Today's Run Summary
                                </h3>


                                <table
                                    width="100%"
                                    cellpadding="0"
                                    cellspacing="0"
                                >

                                    <tr>

                                        <!-- TOTAL SCRAPED -->

                                        <td
                                            width="25%"
                                            style="
                                                text-align:center;
                                                padding:15px;
                                                background:#EBF5FB;
                                                border-radius:8px
                                            "
                                        >

                                            <div style="
                                                font-size:28px;
                                                font-weight:bold;
                                                color:{header_bg}
                                            ">
                                                {summary.get(
                                                    'total_scraped',
                                                    0
                                                )}
                                            </div>

                                            <div style="
                                                font-size:12px;
                                                color:#666;
                                                margin-top:4px
                                            ">
                                                Total ASINs Scraped
                                            </div>

                                        </td>


                                        <td width="3%"></td>


                                        <!-- STOCK FILTER -->

                                        <td
                                            width="25%"
                                            style="
                                                text-align:center;
                                                padding:15px;
                                                background:#EBF5FB;
                                                border-radius:8px
                                            "
                                        >

                                            <div style="
                                                font-size:28px;
                                                font-weight:bold;
                                                color:{accent}
                                            ">
                                                {summary.get(
                                                    'after_filter',
                                                    0
                                                )}
                                            </div>

                                            <div style="
                                                font-size:12px;
                                                color:#666;
                                                margin-top:4px
                                            ">
                                                After Stock Filter
                                            </div>

                                        </td>


                                        <td width="3%"></td>


                                        <!-- QTY FILTER -->

                                        <td
                                            width="25%"
                                            style="
                                                text-align:center;
                                                padding:15px;
                                                background:#EBF5FB;
                                                border-radius:8px
                                            "
                                        >

                                            <div style="
                                                font-size:28px;
                                                font-weight:bold;
                                                color:#F18F01
                                            ">
                                                {summary.get(
                                                    'after_qty_filter',
                                                    0
                                                )}
                                            </div>

                                            <div style="
                                                font-size:12px;
                                                color:#666;
                                                margin-top:4px
                                            ">
                                                Qty 30+ Remaining
                                            </div>

                                        </td>


                                        <td width="3%"></td>


                                        <!-- NEW SUPPRESSIONS -->

                                        <td
                                            width="25%"
                                            style="
                                                text-align:center;
                                                padding:15px;
                                                background:#FDECEA;
                                                border-radius:8px
                                            "
                                        >

                                            <div style="
                                                font-size:28px;
                                                font-weight:bold;
                                                color:#DC3545
                                            ">
                                                {summary.get(
                                                    'new_suppressions',
                                                    0
                                                )}
                                            </div>

                                            <div style="
                                                font-size:12px;
                                                color:#666;
                                                margin-top:4px
                                            ">
                                                New Suppressions
                                            </div>

                                        </td>

                                    </tr>

                                </table>

                            </td>

                        </tr>


                        <!-- ASIN DETAILS -->

                        <tr>

                            <td style="
                                padding:25px 40px
                            ">
                                {asin_table}
                            </td>

                        </tr>


                        <!-- FOOTER -->

                        <tr>

                            <td style="
                                background:#F8F9FA;
                                padding:20px 40px;
                                text-align:center;
                                border-top:1px solid #DEE2E6
                            ">

                                <p style="
                                    color:#6C757D;
                                    font-size:12px;
                                    margin:0
                                ">

                                    📎 Full report attached as Excel file
                                    &nbsp;|&nbsp;

                                    Master suppression file has been
                                    updated automatically

                                    <br>

                                    <strong>
                                        Suppression Monitor
                                    </strong>

                                    · {brand} · {today}

                                </p>

                            </td>

                        </tr>

                    </table>

                </td>

            </tr>

        </table>

    </body>

    </html>
    """

    return html


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    config,
    df_new_suppressions,
    summary,
    attachment_path=None,
    brand="Clicktech"
):
    """
    Send suppression report email using Gmail SMTP SSL.

    Gmail configuration expected in config.json:

    "email": {
        "sender": "your_email@gmail.com",
        "password": "YOUR_GMAIL_APP_PASSWORD",
        "recipients": [
            "recipient@gmail.com"
        ],
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 465
    }
    """

    # -----------------------------------------------------
    # READ CONFIG
    # -----------------------------------------------------

    try:

        sender = config["email"]["sender"]
        password = config["email"]["password"]
        recipients = config["email"]["recipients"]

        smtp_host = config["email"].get(
            "smtp_host",
            "smtp.gmail.com"
        )

        # Force Gmail SSL port 465
        smtp_port = 465

    except KeyError as exc:

        logger.error(
            f"❌ Missing email configuration key: {exc}"
        )

        return False


    # -----------------------------------------------------
    # VALIDATE EMAIL CONFIG
    # -----------------------------------------------------

    if not sender:
        logger.error(
            "❌ Email sender is empty."
        )
        return False

    if not password:
        logger.error(
            "❌ Email password/App Password is empty."
        )
        return False

    if not recipients:
        logger.error(
            "❌ No email recipients configured."
        )
        return False

    if isinstance(recipients, str):
        recipients = [recipients]


    # -----------------------------------------------------
    # EMAIL SUBJECT
    # -----------------------------------------------------

    today = datetime.now().strftime(
        "%d-%b-%Y"
    )

    new_count = len(
        df_new_suppressions
    )

    subject_flag = (
        "🔴 ACTION REQUIRED"
        if new_count > 0
        else "✅ All Clear"
    )

    subject = (
        f"{subject_flag} | "
        f"{brand} Suppression Report | "
        f"{new_count} New | "
        f"{today}"
    )


    # -----------------------------------------------------
    # CREATE EMAIL MESSAGE
    # -----------------------------------------------------

    msg = MIMEMultipart("mixed")

    msg["From"] = (
        f"Suppression Monitor <{sender}>"
    )

    msg["To"] = ", ".join(
        recipients
    )

    msg["Subject"] = subject


    # -----------------------------------------------------
    # PLAIN TEXT BODY
    # -----------------------------------------------------

    suppressed_asins = (
        "\n".join(
            df_new_suppressions["ASIN"]
            .astype(str)
            .tolist()
        )
        if new_count > 0
        else "None"
    )

    plain_text = f"""
{brand} Suppression Report - {today}
{'=' * 50}

New Suppressions Found:
{new_count}

Total ASINs Scraped:
{summary.get('total_scraped', 0)}

After Stock Filter:
{summary.get('after_filter', 0)}

After Inventory Match:
{summary.get('after_inventory_match', 0)}

After Qty Filter (30+):
{summary.get('after_qty_filter', 0)}

New Suppressed ASINs:
{suppressed_asins}

Full report attached.
"""


    # -----------------------------------------------------
    # HTML BODY
    # -----------------------------------------------------

    html_body = build_html_email(
        df_new_suppressions,
        summary,
        brand
    )


    body = MIMEMultipart(
        "alternative"
    )

    body.attach(
        MIMEText(
            plain_text,
            "plain",
            "utf-8"
        )
    )

    body.attach(
        MIMEText(
            html_body,
            "html",
            "utf-8"
        )
    )

    msg.attach(body)


    # -----------------------------------------------------
    # ATTACH EXCEL REPORT
    # -----------------------------------------------------

    if (
        attachment_path
        and os.path.exists(attachment_path)
    ):

        try:

            with open(
                attachment_path,
                "rb"
            ) as file:

                part = MIMEBase(
                    "application",
                    "octet-stream"
                )

                part.set_payload(
                    file.read()
                )

            encoders.encode_base64(
                part
            )

            filename = os.path.basename(
                attachment_path
            )

            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )

            msg.attach(part)

            logger.info(
                f"Attached: {filename}"
            )

        except OSError as exc:

            logger.error(
                f"❌ Could not attach Excel file: {exc}"
            )

            return False

    else:

        logger.warning(
            "⚠️ No valid attachment file was provided."
        )


    # -----------------------------------------------------
    # CONNECT USING SSL / PORT 465
    # -----------------------------------------------------

    server = None

    try:

        logger.info(
            f"Connecting to {smtp_host}:{smtp_port} using SSL..."
        )

        ssl_context = ssl.create_default_context()

        server = smtplib.SMTP_SSL(
            host=smtp_host,
            port=smtp_port,
            timeout=60,
            context=ssl_context
        )

        # Keep SMTP diagnostics enabled for this test
        server.set_debuglevel(1)

        logger.info(
            "✅ SSL connection established."
        )


        # -------------------------------------------------
        # EHLO
        # -------------------------------------------------

        server.ehlo()

        logger.info(
            f"Authenticating as {sender}..."
        )


        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        server.login(
            sender,
            password
        )

        logger.info(
            "✅ SMTP authentication successful."
        )


        # -------------------------------------------------
        # SEND EMAIL
        # -------------------------------------------------

        server.sendmail(
            sender,
            recipients,
            msg.as_string()
        )

        logger.info(
            "✅ Email sent successfully to: "
            + ", ".join(recipients)
        )

        return True


    # -----------------------------------------------------
    # GMAIL AUTH ERROR
    # -----------------------------------------------------

    except smtplib.SMTPAuthenticationError as exc:

        logger.error(
            "❌ Gmail authentication failed."
        )

        logger.error(
            "Make sure the password is a Gmail App Password."
        )

        logger.error(
            "Do NOT use the normal Gmail account password."
        )

        logger.error(
            f"SMTP response: {exc}"
        )

        return False


    # -----------------------------------------------------
    # CONNECTION ERROR
    # -----------------------------------------------------

    except smtplib.SMTPConnectError as exc:

        logger.error(
            f"❌ SMTP connection error: {exc}"
        )

        return False


    # -----------------------------------------------------
    # TIMEOUT
    # -----------------------------------------------------

    except TimeoutError as exc:

        logger.error(
            f"❌ SMTP connection timed out: {exc}"
        )

        return False


    # -----------------------------------------------------
    # NETWORK ERROR
    # -----------------------------------------------------

    except OSError as exc:

        logger.error(
            f"❌ SMTP network error: {exc}"
        )

        logger.error(
            "Check network/security software if "
            "Gmail SSL connection is being blocked."
        )

        return False


    # -----------------------------------------------------
    # SMTP ERROR
    # -----------------------------------------------------

    except smtplib.SMTPException as exc:

        logger.error(
            f"❌ SMTP error: {exc}"
        )

        return False


    # -----------------------------------------------------
    # UNKNOWN ERROR
    # -----------------------------------------------------

    except Exception as exc:

        logger.exception(
            f"❌ Unexpected email error: {exc}"
        )

        return False


    # -----------------------------------------------------
    # CLEANUP
    # -----------------------------------------------------

    finally:

        if server is not None:

            try:
                server.quit()

            except Exception:

                try:
                    server.close()

                except Exception:
                    pass