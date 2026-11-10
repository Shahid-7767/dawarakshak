
import os
import traceback
import io
import qrcode

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    send_file
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


# --------------------------------------------------
# FLASK APPLICATION CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1
)

PUBLIC_BASE_URL = os.environ.get(
    "PUBLIC_BASE_URL",
    "https://pharmatrace-blockchain.onrender.com"
).rstrip("/")


# --------------------------------------------------
# DATABASE AND BLOCKCHAIN INITIALIZATION
# --------------------------------------------------

with app.app_context():
    init_db()
    chain = Blockchain()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

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


# --------------------------------------------------
# REGISTER MEDICINE
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    print("REGISTER ROUTE CALLED", flush=True)

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

        print("REGISTRATION DATA RECEIVED", flush=True)

        try:

            result = register_medicine(data, chain)

            print("REGISTRATION RESULT:", result, flush=True)

            if result["accepted"]:

                flash(
                    "Medicine registered successfully "
                    f"in block {result['block_index']}.",
                    "success"
                )

            else:

                flash(
                    "Transaction rejected: "
                    f"{result['reason']}",
                    "error"
                )

        except Exception as exc:

            print(
                "\n========== MEDICINE REGISTRATION ERROR ==========",
                flush=True
            )

            traceback.print_exc()

            print(
                "=================================================",
                flush=True
            )

            flash(str(exc), "error")

        return redirect(url_for("dashboard"))

    return render_template("register.html")


# --------------------------------------------------
# DYNAMIC QR CODE GENERATION
# --------------------------------------------------

@app.route("/qr/<batch_id>")
def medicine_qr(batch_id):

    medicine = get_medicine(batch_id)

    if not medicine:
        return "Medicine not found", 404

    medicine_path = url_for(
        "medicine_detail",
        batch_id=batch_id
    )

    qr_url = f"{PUBLIC_BASE_URL}{medicine_path}"

    qr = qrcode.make(qr_url)

    qr_buffer = io.BytesIO()

    qr.save(qr_buffer, format="PNG")

    qr_buffer.seek(0)

    print("QR URL:", qr_url, flush=True)

    return send_file(
        qr_buffer,
        mimetype="image/png",
        download_name=f"{secure_filename(batch_id)}.png",
        as_attachment=request.args.get("download") == "1"
    )


# --------------------------------------------------
# MEDICINE VERIFICATION
# --------------------------------------------------

@app.route("/medicine/<batch_id>")
def medicine_detail(batch_id):

    medicine = get_medicine(batch_id)

    if not medicine:

        flash(
            "No registered medicine found "
            "for this batch ID.",
            "error"
        )

        return redirect(url_for("dashboard"))

    return render_template(
        "medicine.html",
        medicine=medicine
    )


# --------------------------------------------------
# CONSENSUS DEMONSTRATION
# --------------------------------------------------

@app.route(
    "/api/consensus/demo",
    methods=["POST"]
)
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


# --------------------------------------------------
# BLOCKCHAIN API
# --------------------------------------------------

@app.route("/api/chain")
def chain_api():

    return jsonify({

        "valid": verify_chain(chain),

        "blocks": [
            block.to_dict()
            for block in chain.blocks
        ]

    })


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "service": "PharmaTrace"
    })


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
