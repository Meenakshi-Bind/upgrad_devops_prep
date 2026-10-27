import json
import re

def lambda_handler(event, context):

    try:
        # Safe parsing
        body = event.get("body", "{}")

        if isinstance(body, str):
            body = json.loads(body)

        password = body.get("password", "")

        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[0-9]", password):
            score += 1
        if re.search(r"[@$!%*?&]", password):
            score += 1

        levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({
                "strength": levels[score-1] if score > 0 else "Very Weak",
                "score": score
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
