import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import time
import hashlib

import sys

# Add project root to path so modules can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import custom modules
from preprocessing.preprocess import preprocess_image
from feature_extraction.resnet_features import ResNetFeatureExtractor
from hashing.perceptual_hash import generate_perceptual_hash, image_to_binary
from encryption.collatz_encryption import encrypt_hash
from watermark.zero_watermark import generate_zero_watermark, xor_hashes, generate_enterprise_watermark
from qr.qr_generator import generate_qr_code, decode_qr_code
from verification.verify_image import ImageVerifier
from robustness_testing.attacks import (
    apply_gaussian_noise, apply_salt_and_pepper, 
    apply_rotation, apply_cropping, apply_jpeg_compression
)
from robustness_testing.metrics import calculate_psnr, calculate_ssim, calculate_ber
from blockchain.ledger import Blockchain

app = Flask(__name__)
app.secret_key = 'medishield_secret_key'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Configuration
UPLOAD_FOLDER = os.path.join('ui', 'static', 'uploads')
RESULTS_FOLDER = os.path.join('ui', 'static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Shared secret key and seed
DEFAULT_SECRET_KEY = "1" * 2048
COLLATZ_SEED = 123

# Initialize extractor globally to avoid reloading ResNet on every request
extractor = ResNetFeatureExtractor()

# Initialize Blockchain
blockchain_file = os.path.join('ui', 'static', 'blockchain_data.json')
blockchain = Blockchain.load_from_file(blockchain_file)

@app.route('/')
def dashboard():
    return render_template('index.html', active_page='dashboard')

@app.route('/register')
def register_page():
    return render_template('generate.html', active_page='register')

@app.route('/verify')
def verify_page():
    return render_template('verify.html', active_page='verify')

@app.route('/robustness')
def robustness_page():
    return render_template('robustness.html', active_page='robustness')

@app.route('/blockchain')
@app.route('/explorer')
def blockchain_page():
    return render_template('blockchain.html', active_page='blockchain', chain=blockchain.chain)

@app.route('/dashboard')
def hospital_dashboard():
    return render_template('hospital_dashboard.html', active_page='dashboard')

@app.route('/history')
def history_page():
    return render_template('blockchain.html', active_page='history', chain=blockchain.chain)

@app.route('/federated')
def federated_page():
    return render_template('federated.html', active_page='federated')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files or 'watermark_logo' not in request.files:
        flash('Both medical image and watermark logo are required', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['image']
    logo_file = request.files['watermark_logo']
    
    if file.filename == '' or logo_file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('index'))
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    logo_filename = secure_filename(logo_file.filename)
    logo_path = os.path.join(UPLOAD_FOLDER, logo_filename)
    logo_file.save(logo_path)
    
    try:
        # Preprocessing
        processed = preprocess_image(filepath)
        
        # Feature Extraction
        features = extractor.extract_features(processed)
        
        # Perceptual Hashing
        p_hash = generate_perceptual_hash(features)
        
        # Encryption
        enc_hash = encrypt_hash(p_hash, seed=COLLATZ_SEED)
        
        # Zero Watermark (Signature) - Linked with Logo and digitally signed with RSA!
        watermark_binary = image_to_binary(logo_path, length=2048)
        hospital_name = request.form.get('hospital', 'City General')
        signature, rsa_signature = generate_enterprise_watermark(enc_hash, watermark_binary, hospital_name)
        
        # QR Generation
        qr_filename = f"qr_{filename.split('.')[0]}.png"
        qr_path = os.path.join(RESULTS_FOLDER, qr_filename)
        generate_qr_code(signature, qr_path)

        # Record on Blockchain JSON Ledger (With new RSA Enterprise signatures)
        transaction = {
            'image_id': request.form.get('image_id', filename),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'signature_hash': hashlib.sha256(signature.encode()).hexdigest(),
            'rsa_signature_hex': rsa_signature[:48] + "..." if len(rsa_signature) > 48 else rsa_signature,
            'hospital': hospital_name,
            'modality': request.form.get('modality', 'X-Ray')
        }
        blockchain.add_new_transaction(transaction)
        blockchain.mine()
        blockchain.save_to_file(blockchain_file)
        
        result = {
            'signature': signature[:256] + "...",
            'qr_path': qr_filename,
            'blockchain_status': "Anchored on block #" + str(blockchain.last_block.index)
        }
        
        flash(f'Watermark generated and anchored on Blockchain (Block {blockchain.last_block.index}).', 'success')
        return render_template('generate.html', active_page='generate', result=result)
        
    except Exception as e:
        flash(f'Error processing image: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/process_verify', methods=['POST'])
def process_verify():
    if 'image' not in request.files or 'qr_code' not in request.files or 'watermark_logo' not in request.files:
        flash('Medical image, QR code, and watermark logo are required', 'danger')
        return redirect(url_for('verify_page'))
    
    img_file = request.files['image']
    qr_file = request.files['qr_code']
    logo_file = request.files['watermark_logo']
    
    img_path = os.path.join(UPLOAD_FOLDER, secure_filename(img_file.filename))
    qr_path = os.path.join(UPLOAD_FOLDER, secure_filename(qr_file.filename))
    logo_path = os.path.join(UPLOAD_FOLDER, secure_filename(logo_file.filename))
    
    img_file.save(img_path)
    qr_file.save(qr_path)
    logo_file.save(logo_path)
    
    try:
        # Generate the secret key (K) from the watermark logo
        watermark_binary = image_to_binary(logo_path, length=2048)
        
        # Use the global extractor to save time
        verifier = ImageVerifier(watermark_binary, COLLATZ_SEED, extractor=extractor)
        
        result_data = verifier.verify(img_path, qr_path)
        
        if result_data['status'] == "Error":
             flash(f"Verification Error: {result_data['message']}", 'danger')
             return redirect(url_for('verify_page'))

        # Blockchain verification check
        sig_hash = hashlib.sha256(result_data['extracted_watermark'].encode()).hexdigest()
        on_chain = False
        block_idx = -1
        
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.get('signature_hash') == sig_hash:
                    on_chain = True
                    block_idx = block.index
                    break
        
        result_data['on_chain'] = on_chain
        result_data['block_index'] = block_idx
        
        if result_data['is_authentic'] and on_chain:
            flash(f'Verification successful: AUTHENTIC and Anchored on Blockchain (Block {block_idx}).', 'success')
        elif result_data['is_authentic']:
            flash('Verification successful: AUTHENTIC (but no on-chain record found).', 'warning')
        else:
            flash('Verification completed: Image appears TAMPERED.', 'danger')
        
        result_data['image_filename'] = secure_filename(img_file.filename)
        
        # Add metadata from blockchain if found
        if on_chain:
            for block in blockchain.chain:
                for tx in block.transactions:
                    if tx.get('signature_hash') == sig_hash:
                        result_data['image_id'] = tx.get('image_id')
                        result_data['timestamp'] = tx.get('timestamp')
                        result_data['tx_hash'] = block.hash
                        break

        return render_template('verify.html', active_page='verify', result=result_data, image_filename=result_data['image_filename'])
        
    except Exception as e:
        flash(f'Verification failed: {str(e)}', 'danger')
        return redirect(url_for('verify_page'))

@app.route('/process_robustness', methods=['POST'])
def process_robustness():
    if 'image' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('robustness_page'))
    
    file = request.files['image']
    attack_req = request.form.get('attack', 'gaussian_0.01')
    
    parts = attack_req.split('_')
    if len(parts) >= 3 and parts[0] == 'salt' and parts[1] == 'pepper':
        attack_type = 'salt_pepper'
        attack_val = float(parts[2])
    else:
        attack_type = parts[0]
        attack_val = float(parts[1]) if len(parts) > 1 else 0

    attack_display_name = {
        'gaussian': f"Gaussian Noise (σ={attack_val})",
        'salt_pepper': f"Salt & Pepper ({attack_val})",
        'rotation': f"Rotation ({int(attack_val)}°)",
        'cropping': f"Center Crop ({int(attack_val)}%)",
        'jpeg': f"JPEG Compression (Q={int(attack_val)})"
    }.get(attack_type, attack_req)
    
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)
    
    try:
        orig_processed = preprocess_image(filepath)
        attacked = orig_processed.copy()
        
        if attack_type == 'gaussian':
            attacked = apply_gaussian_noise(orig_processed, sigma=attack_val)
        elif attack_type == 'salt_pepper':
            attacked = apply_salt_and_pepper(orig_processed, amount=attack_val)
        elif attack_type == 'rotation':
            attacked = apply_rotation(orig_processed, angle=int(attack_val))
        elif attack_type == 'cropping':
            attacked = apply_cropping(orig_processed, percent=int(attack_val))
        elif attack_type == 'jpeg':
            attacked = apply_jpeg_compression(orig_processed, quality=int(attack_val))
        else:
            attacked = orig_processed.copy()
            
        # Save attacked image result
        attack_filename = "attacked.png"
        attack_path = os.path.join(RESULTS_FOLDER, attack_filename)
        cv2.imwrite(attack_path, (attacked * 255).astype(np.uint8))
        
        # Metrics
        p = calculate_psnr(orig_processed, attacked)
        s = calculate_ssim(orig_processed, attacked)
        
        # Compare hashes
        f1 = extractor.extract_features(orig_processed)
        f2 = extractor.extract_features(attacked)
        h1 = generate_perceptual_hash(f1)
        h2 = generate_perceptual_hash(f2)
        ber = calculate_ber(h1, h2)
        
        result = {
            'attack_type': attack_display_name,
            'psnr': p,
            'ssim': s,
            'ber': ber
        }
        
        return render_template('robustness.html', active_page='robustness', result=result)
        
    except Exception as e:
        flash(f'Attack evaluation failed: {str(e)}', 'danger')
        return redirect(url_for('robustness_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

