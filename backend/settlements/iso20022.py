from xml.etree.ElementTree import Element, SubElement, tostring

from django.utils import timezone


def build_camt054_settlement_message(settlement_transaction, message_id):
    order = settlement_transaction.order
    bond = order.bond
    investor = order.investor
    created_at = timezone.now()
    booking_date = settlement_transaction.settled_at or created_at

    document = Element("Document")
    notification = SubElement(document, "BkToCstmrDbtCdtNtfctn")

    group_header = SubElement(notification, "GrpHdr")
    SubElement(group_header, "MsgId").text = message_id
    SubElement(group_header, "CreDtTm").text = created_at.isoformat()

    account_notification = SubElement(notification, "Ntfctn")
    SubElement(account_notification, "Id").text = f"BONDORDER-{order.id}"

    account = SubElement(account_notification, "Acct")
    account_id = SubElement(account, "Id")
    SubElement(account_id, "Othr").text = investor.wallet_address
    SubElement(account, "Nm").text = investor.display_name

    entry = SubElement(account_notification, "Ntry")
    amount = SubElement(entry, "Amt", Ccy=bond.currency)
    amount.text = f"{order.total_amount:.2f}"
    SubElement(entry, "CdtDbtInd").text = "DBIT"
    SubElement(entry, "Sts").text = "BOOK"
    booking = SubElement(entry, "BookgDt")
    SubElement(booking, "DtTm").text = booking_date.isoformat()
    SubElement(entry, "AddtlNtryInf").text = (
        f"Tokenized bond settlement for {order.quantity} {bond.symbol} "
        f"against {order.stablecoin_symbol} on {settlement_transaction.chain}"
    )

    details = SubElement(entry, "NtryDtls")
    transaction_details = SubElement(details, "TxDtls")
    references = SubElement(transaction_details, "Refs")
    SubElement(references, "AcctSvcrRef").text = settlement_transaction.transaction_hash
    SubElement(references, "EndToEndId").text = f"ORDER-{order.id}"

    related_parties = SubElement(transaction_details, "RltdPties")
    debtor = SubElement(related_parties, "Dbtr")
    SubElement(debtor, "Nm").text = investor.display_name
    creditor = SubElement(related_parties, "Cdtr")
    SubElement(creditor, "Nm").text = bond.issuer_name

    remittance = SubElement(transaction_details, "RmtInf")
    block_number = settlement_transaction.block_number or "pending"
    SubElement(remittance, "Ustrd").text = (
        f"Bond={bond.symbol}; ISIN={bond.isin or 'N/A'}; "
        f"Quantity={order.quantity}; Block={block_number}"
    )

    return tostring(document, encoding="unicode")
