// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title MedicalLedger
 * @dev Immutable blockchain registry for Zero-Watermarked Medical Scans.
 * Deploy this to an Ethereum Testnet (Sepolia) or locally via Ganache.
 */
contract MedicalLedger {
    struct MedicalRecord {
        string imageId;
        string hospitalName;
        string modality;
        string zeroWatermarkSignature;
        string rsaDigitalSignature; // Enterprise RSA Validation
        uint256 timestamp;
        bool isRegistered;
    }

    mapping(string => MedicalRecord) public records;
    address public admin;

    event RecordRegistered(string imageId, string hospitalName, uint256 timestamp);

    constructor() {
        admin = msg.sender;
    }

    function registerImage(
        string memory _imageId, 
        string memory _hospitalName, 
        string memory _modality, 
        string memory _signature,
        string memory _rsaSignature
    ) public {
        require(!records[_imageId].isRegistered, "Image ID already registered!");
        
        records[_imageId] = MedicalRecord({
            imageId: _imageId,
            hospitalName: _hospitalName,
            modality: _modality,
            zeroWatermarkSignature: _signature,
            rsaDigitalSignature: _rsaSignature,
            timestamp: block.timestamp,
            isRegistered: true
        });

        emit RecordRegistered(_imageId, _hospitalName, block.timestamp);
    }

    function verifyImage(string memory _imageId) public view returns (
        string memory hospitalName,
        string memory signature,
        string memory rsaSignature,
        uint256 timestamp
    ) {
        require(records[_imageId].isRegistered, "Image not found on blockchain!");
        MedicalRecord memory rec = records[_imageId];
        return (rec.hospitalName, rec.zeroWatermarkSignature, rec.rsaDigitalSignature, rec.timestamp);
    }
}
