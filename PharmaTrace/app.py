
import os
import qrcode

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, jsonify
)

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename

from blockchain.chain import Blockchain
from database.db import init_db
from modules.medicine import (
    register_medicine,
    list_medicines,
    get_medicine
)
from modules.verification import verify_chain
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Support HTTPS headers from Render
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1
)

app.config["PREFERRED_URL_SCHEME"] = "https"


# DATABASE AND BLOCKCHAIN INITIALIZATION
with app.app_context():
    init_db()
    chain = Blockchain()


# QR CODE GENERATION
def generate_qr(medicine_id):
    folder = os.path.join("static", "qr")
    os.makedirs(folder, exist_ok=True)

    safe_id = secure_filename(medicine_id)

    public_base_url = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

    if public_base_url:
        qr_url = (
            f"{public_base_url}/medicine/{medicine_id}"
        )
    else:
        qr_url = url_for(
            "medicine_detail",
            batch_id=medicine_id,
            _external=True,
            _scheme="https"
        )

    qr = qrcode.make(qr_url)

    filename = f"{safe_id}.png"
    filepath = os.path.join(folder, filename)

    qr.save(filepath)

    return filepath


# DASHBOARD
@app.route("/")
def dashboard():

    medicines = list_medicines()

    return render_template(
        "index.html",
        medicines=medicines,
        chain=chain,
        chain_valid=verify_chain(chain),
        validators=chain.consensus.validators
    )


# REGISTER MEDICINE
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        data = {
            "medicine_name": request.form.get(
                "medicine_name", ""
            ).strip(),

            "batch_id": request.form.get(
                "batch_id", ""
            ).strip(),

            "manufacturer": request.form.get(
                "manufacturer", ""
            ).strip(),

            "manufactured_on": request.form.get(
                "manufactured_on", ""
            ).strip(),

            "expires_on": request.form.get(
                "expires_on", ""
            ).strip()
        }

        try:
            result = register_medicine(data, chain)

            if result["accepted"]:

                generate_qr(data["batch_id"])

                flash(
                    "Medicine registered successfully in block "
                    f"{result['block_index']}.",
                    "success"
                )

            else:
                flash(
                    "Transaction rejected: "
                    f"{result['reason']}",
                    "error"
                )

        except (ValueError, Exception) as exc:
            flash(str(exc), "error")

        return redirect(url_for("dashboard"))

    return render_template("register.html")


# MEDICINE VERIFICATION
@app.route("/medicine/<batch_id>")
def medicine_detail(batch_id):

    medicine = get_medicine(batch_id)

    if not medicine:
        flash(
            "No registered medicine found for this batch ID.",
            "error"
        )
        return redirect(url_for("dashboard"))

    return render_template(
        "medicine.html",
        medicine=medicine
    )


# CONSENSUS DEMONSTRATION
@app.route("/api/consensus/demo", methods=["POST"])
def consensus_demo():

    payload = request.get_json(silent=True) or {}

    votes = payload.get(
        "votes",
        [True, True, True, False]
    )

    if (
        not isinstance(votes, list)
        or len(votes) != 4
        or not all(type(vote) is bool for vote in votes)
    ):
        return jsonify({
            "error": "Provide exactly four boolean votes."
        }), 400

    result = chain.consensus.evaluate(votes)

    return jsonify(result)


# BLOCKCHAIN API
@app.route("/api/chain")
def chain_api():

    return jsonify({
        "valid": verify_chain(chain),
        "blocks": [
            block.to_dict()
            for block in chain.blocks
        ]
    })


# HEALTH CHECK
@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "service": "PharmaTrace"
    })


# RUN APPLICATION
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
