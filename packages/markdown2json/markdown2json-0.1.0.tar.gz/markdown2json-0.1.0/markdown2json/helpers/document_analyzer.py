"""Document analysis helper functions"""

from typing import Dict


def extract_header_info(parsed_content: Dict) -> Dict:
    """Extract header information from the document."""
    header_info = {"company_info": {}, "addresses": [], "logo": None}

    for item in parsed_content["content"][:10]:
        if item["type"] == "image":
            header_info["logo"] = item
        elif item["type"] in ["text", "key_value"]:
            if "address" in item.get("semantic_role", ""):
                header_info["addresses"].append(item)
            elif any(
                word in item.get("text", "").lower()
                for word in ["corporation", "inc", "ltd"]
            ):
                header_info["company_info"] = item

    return header_info


def extract_footer_info(parsed_content: Dict) -> Dict:
    """Extract footer information from the document."""
    footer_info = {"payment_info": [], "notes": [], "page_numbers": []}

    for item in reversed(parsed_content["content"]):
        if item["type"] == "text":
            text_lower = item["text"].lower()
            if any(word in text_lower for word in ["payment", "pay"]):
                footer_info["payment_info"].append(item)
            elif "page" in text_lower:
                footer_info["page_numbers"].append(item)
            elif item.get("semantic_role") == "general":
                footer_info["notes"].append(item)

    return footer_info
