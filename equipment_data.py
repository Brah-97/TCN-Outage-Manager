"""
TCN Transmission Equipment Database
Organized by: Region -> SubRegion/ACC -> Substation -> Equipment
Equipment types: Transformer, Transmission Line, Reactor, Capacitor Bank
"""

EQUIPMENT_TYPES = ["Transmission Line", "Transformer", "Reactor", "Capacitor Bank"]

# Each substation maps to a dict of equipment type -> list of equipment names
# Format: {region: {subregion: {substation: {equip_type: [items]}}}}

SUBSTATION_EQUIPMENT = {

    # ===================== ABUJA REGION =====================
    "Abuja": {
        "Abuja Sub-region": {
            "Apo 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3APHTR1)',
                    'TR2 45MVA 132/33kV (3APHTR2)',
                    'TR3 100MVA 132/33kV (3APHTR3)',
                    'TR4 100MVA 132/33kV (3APHTR4)',
                ],
                "Transmission Line": [
                    'Katampe-Apo 132kV Line 1 (3KTP-APO1)',
                    'Katampe-Apo 132kV Line 2 (3KTP-APO2)',
                    'Apo-Karu 132kV Line 1 (3APH-KRU1)',
                    'Gwagwalada-Apo 132kV Line 1 T-off Kukwaba (3GWA-KKB-APH1)',
                    'Gwagwalada-Apo 132kV Line 2 (3GWA-APH2)',
                ],
                "Capacitor Bank": ['60Mvar Capacitor Bank (3APHCX1)'],
            },
            "Karu 132kV": {
                "Transformer": [
                    'TR1 100MVA 132/33kV (3KRUTR1)',
                    'TR2 60MVA 132/33kV (3KRUTR2)',
                ],
                "Transmission Line": [
                    'Apo-Karu 132kV Line 1 (3APH-KRU1)',
                    'Karu-Akwanga T-off Keffi 132kV (3KRU-KEF-AKW1)',
                ],
            },
            "Keffi 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3KEFTR1)',
                    'TR2 60MVA 132/33kV (3KEFTR2)',
                ],
                "Transmission Line": ['Karu-Akwanga T-off Keffi 132kV (3KRU-KEF-AKW1)'],
                "Capacitor Bank": ['25Mvar Capacitor Bank (3KEFCX1)'],
            },
            "Akwanga 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3AKWTR1)',
                    'TR2 40MVA 132/33kV (3AKWTR2)',
                ],
                "Transmission Line": ['Karu-Akwanga T-off Keffi 132kV (3KRU-KEF-AKW1)'],
                "Capacitor Bank": ['20Mvar Capacitor Bank (4AKWCX1)'],
            },
            "Lafia 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3LFATR1)',
                    'TR2 60MVA 132/33kV (3LFATR2)',
                ],
            },
            "Lafia 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2LFATR1)',
                    'TR2 150MVA 330/132kV (2LFATR2)',
                ],
                "Transmission Line": [
                    'Makurdi-Lafia 330kV Line 1 (2MKD-LFA1)',
                    'Makurdi-Lafia 330kV Line 2 (2MKD-LFA2)',
                    'Lafia-Jos 330kV Line 1 (2LFA-JOS1)',
                    'Lafia-Jos 330kV Line 2 (2LFA-JOS2)',
                ],
                "Reactor": ['75Mvar Reactor (2LFARX1)'],
            },
            "Central Area 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3CTATR1)',
                    'TR2 100MVA 132/33kV (3CTATR2)',
                    'TR3 60MVA 132/33kV (3CTATR3)',
                ],
                "Transmission Line": [
                    'Katampe-Central Area 132kV Line 1 (3KTP-KTP-CTA1)',
                    'Katampe-Central Area 132kV Line 2 (3KTP-CTA2)',
                ],
            },
            "Katampe 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2KTPTR1)',
                    'TR2 150MVA 330/132kV (2KTPTR2)',
                    'TR3 150MVA 330/132kV (2KTPTR3)',
                ],
                "Transmission Line": [
                    'Shiroro-Katampe 330kV Line 1 (2SHR-KTP1)',
                    'Gwagwalada-Katampe 330kV Line 1 (2GWA-KTP1)',
                ],
                "Reactor": ['75Mvar Reactor (2KTPRX1)'],
            },
            "Katampe 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KTP1TR1)',
                    'TR2 100MVA 132/33kV (3KTP1TR2)',
                ],
                "Transmission Line": [
                    'Katampe-Apo 132kV Line 1 (3KTP-APO1)',
                    'Katampe-Apo 132kV Line 2 (3KTP-APO2)',
                    'Katampe-Suleja 132kV Line 1 (3KTP-SUL1)',
                    'Katampe-Gwarimpa/Dawaki 132kV Line 1 (3KTP-DWK1)',
                ],
            },
            "Dawaki 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3DWKTR1)',
                    'TR2 60MVA 132/33kV (3DWKTR2)',
                ],
                "Transmission Line": [
                    'Katampe-Gwarimpa/Dawaki 132kV Line 1 (3KTP-DWK1)',
                    'Dawaki-Kubwa 132kV Line 1 (3DWK-KUB1)',
                ],
            },
            "Kubwa 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KUBTR1)',
                    'TR2 100MVA 132/33kV (3KUBTR2)',
                ],
                "Transmission Line": [
                    'Dawaki-Kubwa 132kV Line 1 (3DWK-KUB1)',
                    'Kubwa-Suleja 132kV Line 1 (3KUB-SUL1)',
                ],
            },
            "Katampe 2 132kV": {
                "Transformer": ['TR1 100MVA 132/33kV (3KTP2TR1)'],
            },
            "Geregu 132kV": {
                "Transmission Line": [
                    'Geregu-Ajaokuta 330kV Line 1 (2GER-AJA1)',
                    'Geregu-Ajaokuta 330kV Line 2 (2GER-AJA2)',
                ],
            },
        },
        "Gwagwalada Sub-region": {
            "Suleja 132kV": {
                "Transformer": [
                    'TR1 7.5MVA 132/33kV (3SULTR1)',
                    'TR2 30MVA 132/33kV (3SULTR2)',
                    'TR3 45MVA 132/33kV (3SULTR3)',
                    'TR5 60MVA 132/33kV (3SULTR5)',
                ],
                "Transmission Line": [
                    'Katampe-Suleja 132kV Line 1 (3KTP-SUL1)',
                    'Kubwa-Suleja 132kV Line 1 (3KUB-SUL1)',
                ],
            },
            "Gwagwalada 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2GWATR1)',
                    'TR2 150MVA 330/132kV (2GWATR2)',
                ],
                "Transmission Line": [
                    'Shiroro-Gwagwalada 330kV Line 1 (2SHR-GWA1)',
                    'Lokoja-Gwagwalada 330kV Line 1 (2LKJ-GWA1)',
                    'Lokoja-Gwagwalada 330kV Line 2 (2LKJ-GWA2)',
                    'Gwagwalada-Katampe 330kV Line 1 (2GWA-KTP1)',
                ],
            },
            "Gwagwalada 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3GWATR1)',
                    'TR2 60MVA 132/33kV (3GWATR2)',
                ],
            },
            "Kukwaba 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KKBTR1)',
                    'TR2 60MVA 132/33kV (3KKBTR2)',
                ],
                "Transmission Line": ['Gwagwalada-Apo T-off Kukwaba 132kV (3GWA-KKB-APH1)'],
            },
        },
        "Ajaokuta Sub-region": {
            "Ajaokuta 330kV": {
                "Transformer": [
                    'TR2 162MVA 330/132kV (2AJATR2)',
                    'TR4 162MVA 330/132kV (2AJATR4)',
                ],
                "Transmission Line": [
                    'Ajaokuta-Lokoja 330kV Line 1 (2AJA-LKJ1)',
                    'Ajaokuta-Lokoja 330kV Line 2 (2AJA-LKJ2)',
                    'Geregu-Ajaokuta 330kV Line 1 (2GER-AJA1)',
                    'Geregu-Ajaokuta 330kV Line 2 (2GER-AJA2)',
                ],
                "Reactor": ['35Mvar Reactor (2AJARX1)'],
            },
            "Ajaokuta 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3AJATR1)',
                    'TR2 60MVA 132/33kV (3AJATR2)',
                ],
                "Transmission Line": [
                    'Ajaokuta 330kV-132kV Line 1 (3AJA-AJA1)',
                    'Ajaokuta-Steel Work 132kV Line 1 (3AJA-STW1)',
                    'Ajaokuta-Steel Work 132kV Line 2 (3AJA-STW2)',
                    'Ajaokuta-Okpella T-off Itakpe & Okene 132kV (3AJA-KPE-KNE-KPL1)',
                ],
            },
            "Lokoja 330kV": {
                "Transformer": ['TR1 150MVA 330/132kV (2LKJTR1)'],
                "Transmission Line": [
                    'Ajaokuta-Lokoja 330kV Line 1 (2AJA-LKJ1)',
                    'Ajaokuta-Lokoja 330kV Line 2 (2AJA-LKJ2)',
                    'Lokoja-Gwagwalada 330kV Line 1 (2LKJ-GWA1)',
                    'Lokoja-Gwagwalada 330kV Line 2 (2LKJ-GWA2)',
                ],
                "Reactor": ['75Mvar Reactor (2LKJRX1)'],
            },
            "Lokoja 132kV": {
                "Transformer": ['TR1 60MVA 132/33kV (3LKJTR1)'],
            },
            "Okpella 132kV": {
                "Transformer": [
                    'TR1 15MVA 132/33kV (3KPLTR1)',
                    'TR2 60MVA 132/33kV (3KPLTR2)',
                ],
                "Transmission Line": ['Ajaokuta-Okpella T-off Itakpe & Okene 132kV (3AJA-KPE-KNE-KPL1)'],
            },
            "Okene 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3KNETR1)',
                    'TR2 60MVA 132/33kV (3KNETR2)',
                    'TR3 45MVA 132/33kV (3KNETR3)',
                ],
                "Transmission Line": ['Ajaokuta-Okpella T-off Itakpe & Okene 132kV (3AJA-KPE-KNE-KPL1)'],
            },
        },
    },

    # ===================== BAUCHI REGION =====================
    "Bauchi": {
        "Jos": {
            "Jos 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2JOSTR1)',
                    'TR2 150MVA 330/132kV (2JOSTR2)',
                ],
                "Transmission Line": [
                    'Lafia-Jos 330kV Line 1 (2LFA-JOS1)',
                    'Lafia-Jos 330kV Line 2 (2LFA-JOS2)',
                    'Mando-Jos 330kV Line 1 (2MND-JOS1)',
                ],
                "Reactor": [
                    '75Mvar Reactor 1 (2JOSRX1)',
                    '75Mvar Reactor 2 (2JOSRX2)',
                ],
            },
            "Jos 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3JOSTR1)',
                    'TR3 60MVA 132/33kV (3JOSTR3)',
                ],
                "Transmission Line": [
                    'Jos-Makeri 132kV Line 1 (3JOS-MKR1)',
                    'Jos-Bauchi 132kV Line 1 (3JOS-BAU1)',
                    'Jos-Kafanchan 132kV Line 1 (3JOS-KAF1)',
                ],
            },
            "Makeri 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3MKRTR1)',
                    'TR2 60MVA 132/33kV (3MKRTR2)',
                ],
                "Transmission Line": ['Jos-Makeri 132kV Line 1 (3JOS-MKR1)'],
            },
            "Kafanchan 132kV": {
                "Transformer": ['TR1 40MVA 132/33kV (3KAFTR1)'],
                "Transmission Line": ['Jos-Kafanchan 132kV Line 1 (3JOS-KAF1)'],
            },
        },
        "Bauchi": {
            "Bauchi 132kV": {
                "Transformer": [
                    'TR5 60MVA 132/33kV (3BAUTR5)',
                    'TR2 60/75MVA 132/33kV (3BAUTR2)',
                ],
                "Transmission Line": [
                    'Gombe-Bauchi 132kV Line 1 (3GMB-BAU1)',
                    'Jos-Bauchi 132kV Line 1 (3JOS-BAU1)',
                ],
            },
        },
        "Gombe": {
            "Gombe 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2GMBTR1)',
                    'TR2 150MVA 330/132kV (2GMBTR2)',
                ],
                "Transmission Line": [
                    'Jos-Gombe 330kV Line 1 (2JOS-GMB1)',
                    'Gombe-Damaturu 330kV Line 1 (2GMB-DTR1)',
                    'Gombe-Yola 330kV Line 1 (2GMB-YLA1)',
                ],
                "Reactor": [
                    '50Mvar Reactor 1 (2GMBRX1)',
                    '50Mvar Reactor 2 (2GMBRX2)',
                ],
            },
            "Gombe 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3GMBTR1)',
                    'TR2 60MVA 132/33kV (3GMBTR2)',
                    'TR3 100MVA 132/33kV (3GMBTR3)',
                ],
                "Transmission Line": [
                    'Gombe-Bauchi 132kV Line 1 (3GMB-BAU1)',
                    'Gombe-Billiri-Savannah 132kV (3GMB-BLR-SAV1)',
                    'Gombe-Ashaka-Potiskum 132kV (3GMB-ASH-PTK1)',
                    'Gombe-Dadinkowa-Biu 132kV (3GMB-DKW-BIU1)',
                ],
            },
            "Potiskum 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3PTKTR1)',
                    'TR3 60MVA 132/33kV (3PTKTR3)',
                ],
                "Transmission Line": ['Gombe-Ashaka-Potiskum 132kV (3GMB-ASH-PTK1)'],
            },
            "Biu 132kV": {
                "Transformer": [
                    'TR1 15MVA 132/33kV (3BIUTR1)',
                    'TR2 30MVA 132/33kV (3BIUTR2)',
                    'TR3 60MVA 132/33kV (3BIUTR3)',
                ],
                "Transmission Line": ['Gombe-Dadinkowa-Biu 132kV (3GMB-DKW-BIU1)'],
            },
        },
        "Yola": {
            "Yola 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2YLATR1)',
                    'TR2 150MVA 330/132kV (2YLATR2)',
                    'TR3 150MVA 330/132kV (2YLATR3)',
                ],
                "Transmission Line": ['Gombe-Yola 330kV Line 1 (2GMB-YLA1)'],
                "Reactor": ['75Mvar Reactor (2MLARX1)'],
            },
            "Damaturu 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2DTRTR1)',
                    'TR2 150MVA 330/132kV (2DTRTR2)',
                ],
                "Transmission Line": [
                    'Gombe-Damaturu 330kV Line 1 (2GMB-DTR1)',
                    'Damaturu-Molai 330kV Line 1 (2DTR-MLA1)',
                ],
                "Reactor": ['75Mvar Reactor (2DTRRX1)'],
            },
            "Maiduguri 132kV": {
                "Transformer": [
                    'TR1 (3MDRTR1)',
                    'TR2 (3MDRTR2)',
                ],
            },
            "Molai 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2MLATR1)',
                    'TR2 150MVA 330/132kV (2MLATR2)',
                ],
                "Transmission Line": ['Damaturu-Molai 330kV Line 1 (2DTR-MLA1)'],
                "Reactor": ['75Mvar Reactor (2MLARX1)'],
            },
        },
    },

    # ===================== BENIN REGION =====================
    "Benin": {
        "Benin South Sub-region": {
            "Benin 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2BENTR1)',
                    'TR2 300MVA 330/132kV (2BENTR2)',
                ],
                "Transmission Line": [
                    'Benin-Egbin 330kV Line 1 (2BEN-EGB1)',
                    'Benin-Omotosho 330kV Line 1 (2BEN-MTS1)',
                    'Ihovbor-Benin 330kV Line 1 (2HVR-BEN1)',
                    'Sapele-Benin 330kV Line 1 (2SAP-BEN1)',
                    'Sapele-Benin 330kV Line 2 (2SAP-BEN2)',
                    'Sapele-Benin 330kV Line 3 (2SAP-BEN3)',
                    'Delta-Benin 330kV Line 1 (2UGH-BEN1)',
                    'Benin-Onitsha 330kV Line 1 (2BEN-NSH1)',
                    'Benin-Onitsha 330kV Line 2 (2BEN-NSH2)',
                    'Benin-Asaba 330kV Line 1 (2BEN-ASB1)',
                    'Benin-Ajaokuta 330kV Line 1 (2BEN-AJA1)',
                    'Benin-Ajaokuta 330kV Line 2 (2BEN-AJA2)',
                ],
            },
            "Benin 132kV": {
                "Transformer": [
                    'TR1 100MVA 132/33kV (3BENTR1)',
                    'TR2 80MVA 132/33kV (3BENTR2)',
                    'TR3 60MVA 132/33kV (3BENTR3)',
                    'TR4 60MVA 132/33kV (3BENTR4)',
                ],
                "Transmission Line": [
                    'Benin-Oghara 132kV Line 1 (3BEN-GHA1)',
                    'Benin-Amukpe 132kV Line 1 (3BEN-AMK1)',
                    'Benin-Irrua-Etsako 132kV Line 1 (3BEN-RRU-ESK1)',
                ],
            },
            "Irrua 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3RRUTR1)',
                    'TR2 30MVA 132/33kV (3RRUTR2)',
                ],
                "Transmission Line": ['Benin-Irrua-Etsako 132kV Line 1 (3BEN-RRU-ESK1)'],
            },
            "Etsako 132kV": {
                "Transformer": ['TR1 40MVA 132/33kV (3ESKTR1)'],
                "Transmission Line": ['Benin-Irrua-Etsako 132kV Line 1 (3BEN-RRU-ESK1)'],
            },
            "Oghara 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3GHATR1)',
                    'TR2 30MVA 132/33kV (3GHATR2)',
                ],
                "Transmission Line": [
                    'Benin-Oghara 132kV Line 1 (3BEN-GHA1)',
                    'Delta-Oghara 132kV Line 1 (3UGH-GHA1)',
                ],
            },
            "Amukpe 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3AMKTR1)',
                    'TR2 60MVA 132/33kV (3AMKTR2)',
                ],
                "Transmission Line": [
                    'Benin-Amukpe 132kV Line 1 (3BEN-AMK1)',
                    'Delta-Amukpe 132kV Line 1 (3UGH-AMK1)',
                ],
            },
        },
        "Delta Sub-region": {
            "Delta 330kV": {
                "Transformer": ['TR1 165MVA 330/132kV (2UGHTR1)'],
                "Transmission Line": [
                    'Delta-Benin 330kV Line 1 (2UGH-BEN1)',
                    'Sapele-Delta 330kV Line 1 (2SAP-UGH1)',
                ],
            },
            "Delta 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3UGHTR1)',
                    'TR3 60MVA 132/33kV (3UGHTR3)',
                ],
                "Transmission Line": [
                    'Delta-Oghara 132kV Line 1 (3UGH-GHA1)',
                    'Delta-Amukpe 132kV Line 1 (3UGH-AMK1)',
                    'Delta-Effurun 132kV Line 1 (3UGH-EFR1)',
                    'Delta-Afiesere 132kV Line 1 (3UGH-AFS1)',
                    'Delta-Ozoro 132kV Line 1 (3UGH-ZOR1)',
                ],
            },
            "Effurun 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3EFRTR1)',
                    'TR2 100MVA 132/33kV (3EFRTR2)',
                    'TR3 60MVA 132/33kV (3EFRTR3)',
                ],
                "Transmission Line": ['Delta-Effurun 132kV Line 1 (3UGH-EFR1)'],
            },
            "Afiesere 132kV": {
                "Transformer": ['TR1 30MVA 132/33kV (3AFSTR1)'],
                "Transmission Line": ['Delta-Afiesere 132kV Line 1 (3UGH-AFS1)'],
            },
            "Sapele 330kV": {
                "Transmission Line": [
                    'Sapele-Delta 330kV Line 1 (2SAP-UGH1)',
                    'Sapele-Benin 330kV Line 1 (2SAP-BEN1)',
                    'Sapele-Benin 330kV Line 2 (2SAP-BEN2)',
                    'Sapele-Benin 330kV Line 3 (2SAP-BEN3)',
                ],
            },
        },
        "Ihovbor Work Centre": {
            "Ihovbor 330kV": {
                "Transformer": ['TR1 150MVA 330/132kV (2HVRTR1)'],
                "Transmission Line": [
                    'Ihovbor-Benin 330kV Line 1 (2HVR-BEN1)',
                    'Ihovbor-Osogbo 330kV Line 1 (2HVR-SGB1)',
                ],
            },
            "Ihovbor 132kV": {
                "Transformer": [
                    'TR1 100MVA 132/33kV (3HVRTR1)',
                    'TR2 60MVA 132/33kV (3HVRTR2)',
                ],
                "Transmission Line": [
                    'Ihovbor-Okada 132kV Line 1 (3HVR-KDA1)',
                    'Ihovbor-Okada 132kV Line 2 (3HVR-KDA2)',
                ],
            },
            "Okada 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3KDATR1)',
                    'TR2 40MVA 132/33kV (3KDATR2)',
                ],
                "Transmission Line": [
                    'Ihovbor-Okada 132kV Line 1 (3HVR-KDA1)',
                    'Ihovbor-Okada 132kV Line 2 (3HVR-KDA2)',
                ],
            },
        },
        "Omotosho Sub-region": {
            "Omotosho 330kV": {
                "Transformer": ['TR1 150MVA 330/132kV (2MTSTR1)'],
                "Transmission Line": [
                    'Benin-Omotosho 330kV Line 1 (2BEN-MTS1)',
                    'Omotosho-Ikeja West 330kV Line 1 (2MTS-KJW1)',
                ],
            },
            "Omotosho 132kV": {
                "Transformer": ['TR1 40/44MVA 132/33kV (3MTSTR1)'],
                "Transmission Line": [
                    'Omotosho-Erinje 132kV Line 1 (3MTS-ERJ1)',
                    'Omotosho-Erinje 132kV Line 2 (3MTS-ERJ2)',
                ],
            },
            "Erinje 132kV": {
                "Transformer": [
                    'TR1 30/40MVA 132/33kV (3ERJTR1)',
                    'TR2 30/40MVA 132/33kV (3ERJTR2)',
                ],
                "Transmission Line": [
                    'Omotosho-Erinje 132kV Line 1 (3MTS-ERJ1)',
                    'Omotosho-Erinje 132kV Line 2 (3MTS-ERJ2)',
                ],
            },
            "Ondo 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3NNDTR1)',
                    'TR2 60MVA 132/33kV (3NNDTR2)',
                ],
                "Transmission Line": ['Osogbo-Ilesha-Ife-Ondo 132kV (3SGB-LES-FFE-NND1)'],
            },
        },
    },

    # ===================== ENUGU REGION =====================
    "Enugu": {
        "Enugu Sub-region": {
            "New-Haven 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132/33kV (2NHVTR1)',
                    'TR2 150MVA 330/132/33kV (2NHVTR2)',
                    'TR3 150MVA 330/132/33kV (2NHVTR3)',
                    'TR4 150MVA 330/132/33kV (2NHVTR4)',
                ],
                "Transmission Line": [
                    'Onitsha-New Haven 330kV Line 1 (2NSH-NHV1)',
                    'New Haven-Ugwuaji 330kV Line 1 (2NHV-UGW1)',
                    'New Haven-Ugwuaji 330kV Line 2 (2NHV-UGW2)',
                ],
            },
            "New-Haven 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3NHVTR1)',
                    'TR2 60MVA 132/33kV (3NHVTR2)',
                    'TR3 125MVA 132/33kV (3NHVTR3)',
                    'TR4 125MVA 132/33kV (3NHVTR4)',
                ],
                "Transmission Line": [
                    'New Haven-Nkalagu 132kV Line 1 (3NHV-NKG1)',
                    'New Haven-Nkalagu 132kV Line 2 (3NHV-NKG2)',
                    'New Haven-Nsukka T-off Otukpo 132kV (3NHV-NSK-TKP)',
                    'New Haven-Oji River-Agu Awka 132kV (3NHV-JRV-AGU-AWK1)',
                ],
            },
            "Nkalagu 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3NKGTR1)',
                    'TR2 60MVA 132/33kV (3NKGTR2)',
                ],
                "Transmission Line": [
                    'New Haven-Nkalagu 132kV Line 1 (3NHV-NKG1)',
                    'New Haven-Nkalagu 132kV Line 2 (3NHV-NKG2)',
                    'Nkalagu-Abakaliki 132kV Line 1 (3NKG-ABK1)',
                    'Nkalagu-Abakaliki 132kV Line 2 (3NKG-ABK2)',
                    'Nkalagu-Abakaliki 132kV Line 3 (3NKG-ABK3)',
                ],
            },
            "Abakaliki 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3ABKTR1)',
                    'TR2 60MVA 132/33kV (3ABKTR2)',
                ],
                "Transmission Line": [
                    'Nkalagu-Abakaliki 132kV Line 1 (3NKG-ABK1)',
                    'Nkalagu-Abakaliki 132kV Line 2 (3NKG-ABK2)',
                    'Nkalagu-Abakaliki 132kV Line 3 (3NKG-ABK3)',
                ],
            },
            "UNN Nsukka 132kV": {
                "Transformer": ['TR1 30/40MVA 132/33kV (3NSKTR1)'],
                "Transmission Line": ['New Haven-Nsukka T-off Otukpo 132kV (3NHV-NSK-TKP)'],
            },
            "Ugwuaji 330kV": {
                "Transformer": ['TR1 150MVA 330/132/33kV (2UGWTR1)'],
                "Transmission Line": [
                    'Ikot-Ekpene-Ugwuaji 330kV Line 1 (2KOT-UGW1)',
                    'Ikot-Ekpene-Ugwuaji 330kV Line 2 (2KOT-UGW2)',
                    'Ikot-Ekpene-Ugwuaji 330kV Line 3 (2KOT-UGW3)',
                    'Ikot-Ekpene-Ugwuaji 330kV Line 4 (2KOT-UGW4)',
                    'New Haven-Ugwuaji 330kV Line 1 (2NHV-UGW1)',
                    'New Haven-Ugwuaji 330kV Line 2 (2NHV-UGW2)',
                    'Ugwuaji-Apir 330kV Line 1 (2UGW-APR1)',
                    'Ugwuaji-Apir 330kV Line 2 (2UGW-APR2)',
                ],
            },
            "Ugwuaji 132kV": {
                "Transformer": [
                    'TR3 60MVA 132/33kV (3UGWTR3)',
                    'TR4 60MVA 132/33kV (3UGWTR4)',
                ],
            },
        },
        "Onitsha Sub-region": {
            "Awka 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3AWKTR1)',
                    'TR2 30MVA 132/33kV (3AWKTR2)',
                ],
            },
            "Onitsha 330kV": {
                "Transformer": [
                    'TR1 90MVA 330/132/13.8kV (2NSHTR1)',
                    'TR2 150MVA 330/132kV (2NSHTR2)',
                    'TR3 150MVA 330/132kV (2NSHTR3)',
                ],
                "Transmission Line": [
                    'Ikot-Ekpene-Onitsha 330kV Line 1 (2KPA-NSH1)',
                    'Ikot-Ekpene-Onitsha 330kV Line 2 (2KPA-NSH2)',
                    'Alaoji-Onitsha 330kV Line 1 (2ALJ-NSH1)',
                    'Onitsha-Asaba 330kV Line 1 (2NSH-ASB1)',
                    'Benin-Onitsha 330kV Line 1 (2BEN-NSH1)',
                    'Benin-Onitsha 330kV Line 2 (2BEN-NSH2)',
                    'Onitsha-New Haven 330kV Line 1 (2NSH-NHV1)',
                ],
            },
            "Onitsha 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3NSHTR1)',
                    'TR2 15MVA 132/11kV (3NSHTR2)',
                    'TR3 60MVA 132/33kV (3NSHTR3)',
                    'TR4 60MVA 132/33kV (3NSHTR4)',
                    'TR5 45MVA 132/33kV (3NSHTR5)',
                    'TR6 100MVA 132/33kV (3NSHTR6)',
                    'TR7 75MVA 132/33kV (3NSHTR7)',
                ],
                "Transmission Line": [
                    'Onitsha-GCM 132kV Line 1 (3NSH-GCM1)',
                    'Onitsha-Awka-Agu Awka-Oji River 132kV (3NSH-AWK-AGU-JRV1)',
                ],
            },
            "Agu Awka 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3AGUTR1)',
                    'TR2 60MVA 132/33kV (3AGUTR2)',
                ],
                "Transmission Line": ['Agu Awka-Oji River 132kV Line 1 (3AGU-JRV1)'],
            },
            "GCM 132kV": {
                "Transformer": ['TR1 60MVA 132/33kV (3GCMTR1)'],
                "Transmission Line": ['Onitsha-GCM 132kV Line 1 (3NSH-GCM1)'],
            },
            "Oji River 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3JRVTR1)',
                    'TR2 75MVA 132/33kV (3JRVTR2)',
                    'TR3 60MVA 132/66/33kV (3JRVTR3)',
                ],
                "Transmission Line": [
                    'Onitsha-Awka-Agu Awka-Oji River 132kV (3NSH-AWK-AGU-JRV1)',
                    'Oji River-New Haven 132kV Line 1 (3JRV-NHV1)',
                ],
            },
        },
        "Apir Sub-region": {
            "Kashimbilla 132kV": {
                "Transformer": [
                    'TR1 (3KSLTR1)',
                    'TR2 (3KSLTR2)',
                ],
                "Transmission Line": [
                    'Kashimbilla-Takum 132kV Line 1 (3KSL-TKM1)',
                    'Kashimbilla-Takum 132kV Line 2 (3KSL-TKM2)',
                ],
            },
            "Apir 330kV": {
                "Transformer": ['TR2 330/132kV (2APRTR2)'],
                "Transmission Line": [
                    'Ugwuaji-Apir 330kV Line 1 (2UGW-APR1)',
                    'Ugwuaji-Apir 330kV Line 2 (2UGW-APR2)',
                    'Apir-Lafia 330kV Line 1 (2APR-LFA1)',
                    'Apir-Lafia 330kV Line 2 (2APR-LFA2)',
                ],
            },
            "Apir 132kV": {
                "Transformer": [
                    'TR1 132/33kV (3APRTR1)',
                    'TR2 132/33kV (3APRTR2)',
                    'TR3 MOBITRA (3APRTR3)',
                ],
                "Transmission Line": ['Apir-Yandev-Otukpo 132kV (3APR-YDV-TKP)'],
            },
            "Otukpo 132kV": {
                "Transformer": [
                    'TR1 (3TKPTR1)',
                    'TR2 (3TKPTR2)',
                    'TR3 (3TKPTR3)',
                ],
                "Transmission Line": ['Apir-Yandev-Otukpo 132kV (3APR-TKP-YDV)'],
            },
            "Yandev 132kV": {
                "Transformer": [
                    'TR1 (3YDVTR1)',
                    'TR2 (3YDVTR2)',
                    'TR3 (3YDVTR3)',
                ],
                "Transmission Line": [
                    'Yandev-Wukari 132kV Line 1 (3YDV-WKR1)',
                    'Yandev-Wukari 132kV Line 2 (3YDV-WKR2)',
                ],
            },
            "Wukari 132kV": {
                "Transformer": [
                    'TR1 (3WKRTR1)',
                    'TR2 (3WKRTR2)',
                ],
                "Transmission Line": [
                    'Yandev-Wukari 132kV Line 1 (3YDV-WKR1)',
                    'Yandev-Wukari 132kV Line 2 (3YDV-WKR2)',
                    'Takum-Wukari 132kV Line 1 (3TKM-WKR1)',
                    'Takum-Wukari 132kV Line 2 (3TKM-WKR2)',
                ],
            },
            "Takum 132kV": {
                "Transformer": [
                    'TR1 (3TKMTR1)',
                    'TR2 (3TKMTR2)',
                ],
                "Transmission Line": [
                    'Takum-Wukari 132kV Line 1 (3TKM-WKR1)',
                    'Takum-Wukari 132kV Line 2 (3TKM-WKR2)',
                    'Kashimbilla-Takum 132kV Line 1 (3KSL-TKM1)',
                    'Kashimbilla-Takum 132kV Line 2 (3KSL-TKM2)',
                ],
            },
        },
        "Asaba Work Centre": {
            "Agbor 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3AGBTR1)',
                    'TR2 60MVA 132/33kV (3AGBTR2)',
                ],
                "Transmission Line": [
                    'Asaba-Agbor 132kV Line 1 (3ASB-AGB1)',
                    'Asaba-Agbor 132kV Line 2 (3ASB-AGB2)',
                ],
            },
            "Asaba 330kV": {
                "Transformer": [
                    'TR1 300MVA 330/132/33kV (2ASBTR1)',
                    'TR2 150MVA 330/132kV (2ASBTR2)',
                ],
                "Transmission Line": [
                    'Onitsha-Asaba 330kV Line 1 (2NSH-ASB1)',
                    'Benin-Asaba 330kV Line 1 (2BEN-ASB1)',
                ],
            },
            "Asaba 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3ASBTR1)',
                    'TR2 60MVA 132/33kV (3ASBTR2)',
                ],
                "Transmission Line": [
                    'Asaba-Agbor 132kV Line 1 (3ASB-AGB1)',
                    'Asaba-Agbor 132kV Line 2 (3ASB-AGB2)',
                ],
            },
        },
    },

    # ===================== KADUNA REGION =====================
    "Kaduna": {
        "Kaduna Sub-region": {
            "Mando 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2MNDTR1)',
                    'TR2 90MVA 330/132kV (2MNDTR2)',
                    'TR3 150MVA 330/132kV (2MNDTR3)',
                    'TR4 150MVA 330/132kV (2MNDTR4)',
                    'TR5 150MVA 330/132kV (2MNDTR5)',
                ],
                "Transmission Line": [
                    'Shiroro-Mando 330kV Line 1 (2SHR-MND1)',
                    'Shiroro-Mando 330kV Line 2 (2SHR-MND2)',
                    'Mando-Kumbotso 330kV Line 1 (2MND-KBT1)',
                    'Mando-Jos 330kV Line 1 (2MND-JOS1)',
                ],
                "Reactor": ['75Mvar Reactor (2MNDRX3)'],
            },
            "Mando 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3MNDTR1)',
                    'TR2 60MVA 132/33kV (3MNDTR2)',
                    'TR3 60MVA 132/33kV (3MNDTR3)',
                    'TR4 60MVA 132/33kV (3MNDTR4)',
                ],
                "Transmission Line": [
                    'Mando-Kaduna Town 132kV Line 1 (3MND-KDT1)',
                    'Mando-Kaduna Town 132kV Line 2 (3MND-KDT2)',
                    'Mando-Zaria 132kV Line 1 (3MND-ZAR1)',
                    'Mando-Mando Town 132kV Line 1 (3MND-MND1)',
                ],
            },
            "Kaduna Town 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KDTTR1)',
                    'TR3 60MVA 132/33kV (3KDTTR3)',
                    'TR4 60MVA 132/33kV (3KDTTR4)',
                ],
                "Transmission Line": [
                    'Mando-Kaduna Town 132kV Line 1 (3MND-KDT1)',
                    'Mando-Kaduna Town 132kV Line 2 (3MND-KDT2)',
                ],
                "Capacitor Bank": ['2 x 10Mvar Capacitor Bank'],
            },
            "Zaria 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3ZARTR1)',
                    'TR2 60MVA 132/33kV (3ZARTR2)',
                    'TR3 60MVA 132/33kV (3ZARTR3)',
                    'TR4 40MVA 132/33kV (3ZARTR4)',
                ],
                "Transmission Line": [
                    'Mando-Zaria 132kV Line 1 (3MND-ZAR1)',
                    'Zaria-Funtua 132kV Line 1 (3ZAR-FTA1)',
                    'Zaria-Konar Dangora 132kV Line 1 (3ZAR-KDG1)',
                ],
            },
        },
        "Gusau Works Centre": {
            "Funtua 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3FTATR1)',
                    'TR2 30MVA 132/33kV (3FTATR2)',
                ],
                "Transmission Line": ['Zaria-Funtua 132kV Line 1 (3ZAR-FTA1)'],
            },
        },
        "Birnin Kebbi Sub-region": {
            "Sokoto 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3SOKTR1)',
                    'TR2 30MVA 132/33kV (3SOKTR2)',
                    'TR3 30MVA 132/33kV (3SOKTR3)',
                ],
                "Transmission Line": [
                    'Sokoto-Birnin Kebbi 132kV Line 1 (3BRK-SOK1)',
                    'Sokoto-Talata Mafara 132kV Line 1 (3SOK-TMA1)',
                ],
            },
            "Birnin Kebbi 330kV": {
                "Transformer": [
                    'TR2 150MVA 330/132/33kV (2BRKTR2)',
                    'TR3 150MVA 330/132/33kV (2BRKTR3)',
                ],
                "Transmission Line": ['Birnin Kebbi-Kainji 330kV Line 1 (2BRK-KNJ1)'],
            },
            "Birnin Kebbi 132kV": {
                "Transformer": [
                    'TR4 60MVA 132/33kV (3BRKTR4)',
                    'TR5 60MVA 132/33kV (3BRKTR5)',
                ],
                "Transmission Line": [
                    'Birnin Kebbi-Niamey 132kV Line (3BRK-NYM1)',
                    'Birnin Kebbi-Sokoto 132kV Line 1 (3BRK-SOK1)',
                ],
            },
        },
    },

    # ===================== KANO REGION =====================
    "Kano": {
        "Kano Sub-region": {
            "Kumbotso 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2KBTTR1)',
                    'TR2 150MVA 330/132kV (2KBTTR2)',
                    'TR3 150MVA 330/132kV (2KBTTR3)',
                    'TR4 150MVA 330/132kV (2KBTTR4)',
                    'TR5 300MVA 330/132kV (2KBTTR5)',
                ],
                "Transmission Line": ['Mando-Kumbotso 330kV Line 1 (2MND-KBT1)'],
            },
            "Kumbotso 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KBTTR1)',
                    'TR2 60MVA 132/33kV (3KBTTR2)',
                    'TR4 100MVA 132/33kV (3KBTTR4)',
                ],
                "Transmission Line": [
                    "Kumbotso-Dan'agundi 132kV Line 1 (3KBT-DNG1)",
                    'Kumbotso-Dakata 132kV Line 1 (3KBT-DKT1)',
                    'Kumbotso-Tamburawa 132kV Line 1 (3KBT-TAM1)',
                    'Kumbotso-Dutse-Azare 132kV Line 1 (3KBT-DUT-AZR1)',
                    'Kumbotso-Wudil-Azare 132kV Line 1 (3KBT-WDL-AZR1)',
                    'Kumbotso-Gagarawa-Hadejia 132kV Line 1 (3KBT-GGW-HDJ1)',
                    'Kumbotso-Kankia-Katsina-Daura 132kV (3KBT-KNK-KTN-DRA1)',
                    'Kumbotso-Katsina-Gazaoua 132kV (3KBT-KTN-GAZ1)',
                ],
            },
            "Tamburawa 132kV": {
                "Transformer": [
                    'TR1 30/40MVA 132/33kV (3TAMTR1)',
                    'TR2 30/40MVA 132/33kV (3TAMTR2)',
                ],
                "Transmission Line": ['Kumbotso-Tamburawa 132kV Line 1 (3KBT-TAM1)'],
            },
            "Kwanar-Dangora 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3KDGTR1)',
                    'TR2 63MVA 132/33kV (3KDGTR2)',
                ],
                "Transmission Line": ['Zaria-Konar Dangora 132kV Line 1 (3ZAR-KDG1)'],
            },
            "Wudil 132kV": {
                "Transformer": ['TR1 40MVA 132/33kV (3WDLTR1)'],
                "Transmission Line": ['Kumbotso-Wudil-Azare 132kV Line 1 (3KBT-WDL-AZR1)'],
            },
            "Dan'agundi 132kV": {
                "Transformer": [
                    'TR3 60MVA 132/33kV (3DNGTR3)',
                    'TR4 100/125MVA 132/33kV (3DNGTR4)',
                ],
                "Transmission Line": ["Kumbotso-Dan'agundi 132kV Line 1 (3KBT-DNG1)"],
            },
            "Dakata 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3DKTTR1)',
                    'TR2 60MVA 132/33kV (3DKTTR2)',
                    'TR3 30MVA 132/33kV (3DKTTR3)',
                    'TR4 100/125MVA 132/33kV (3DKTTR4)',
                ],
                "Transmission Line": ['Kumbotso-Dakata 132kV Line 1 (3KBT-DKT1)'],
            },
        },
        "Katsina Sub-region": {
            "Katsina 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3KTNTR1)',
                    'TR2 30MVA 132/33kV (3KTNTR2)',
                    'TR3 30MVA 132/33kV (3KTNTR3)',
                    'TR4 60MVA 132/33kV (3KTNTR4)',
                ],
                "Transmission Line": [
                    'Kumbotso-Kankia-Katsina-Daura 132kV (3KBT-KNK-KTN-DRA1)',
                    'Kumbotso-Katsina-Gazaoua 132kV (3KBT-KTN-GAZ1)',
                ],
            },
            "Daura 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3DRATR1)',
                    'TR2 40MVA 132/33kV (3DRATR2)',
                ],
                "Transmission Line": ['Kumbotso-Kankia-Katsina-Daura 132kV (3KBT-KNK-KTN-DRA1)'],
            },
            "Kankia 132kV": {
                "Transformer": [
                    'TR1 60/75MVA 132/33kV (3KNKTR1)',
                    'TR2 30MVA 132/33kV (3KNKTR2)',
                    'TR3 60/75MVA 132/33kV (3KNKTR3)',
                ],
            },
        },
        "Dutse Sub-region": {
            "Azare 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3AZRTR1)',
                    'TR3 40MVA 132/33kV (3AZRTR3)',
                ],
                "Transmission Line": [
                    'Kumbotso-Dutse-Azare 132kV Line 1 (3KBT-DUT-AZR1)',
                    'Kumbotso-Wudil-Azare 132kV Line 1 (3KBT-WDL-AZR1)',
                ],
            },
            "Dutse 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3DUTTR1)',
                    'TR2 40MVA 132/33kV (3DUTTR2)',
                ],
                "Transmission Line": ['Kumbotso-Dutse-Azare 132kV Line 1 (3KBT-DUT-AZR1)'],
            },
            "Gagarawa 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3GGWTR1)',
                    'TR2 60MVA 132/33kV (3GGWTR2)',
                ],
                "Transmission Line": ['Kumbotso-Gagarawa-Hadejia 132kV (3KBT-GGW-HDJ1)'],
            },
            "Hadejia 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3HDJTR1)',
                    'TR3 60MVA 132/33kV (3HDJTR3)',
                ],
                "Transmission Line": ['Kumbotso-Gagarawa-Hadejia 132kV (3KBT-GGW-HDJ1)'],
            },
        },
    },

    # ===================== LAGOS REGION =====================
    "Lagos": {
        "Aja Sub-Region": {
            "Aja 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2AJATR1)',
                    'TR2 150MVA 330/132kV (2AJATR2)',
                    'TR3 150MVA 330/132kV (2AJATR3)',
                ],
                "Transmission Line": [
                    'Egbin-Aja 330kV Line 1 (3EGN-AJA1)',
                    'Egbin-Aja 330kV Line 2 (3EGN-AJA2)',
                ],
            },
            "Aja 132kV": {
                "Transformer": [
                    'TR1 66MVA 132/33kV (3AJATR1)',
                    'TR2 60MVA 132/33kV (3AJATR2)',
                    'TR3 100MVA 132/33kV (3AJATR3)',
                    'TR4 63MVA 132/33kV (3AJATR4)',
                ],
            },
            "Lekki 132kV": {
                "Transformer": [
                    'TR1 132/33kV',
                    'TR2 132/33kV',
                ],
            },
            "Alagbon 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3ALATR1)',
                    'TR3 100MVA 132/33kV (3ALATR3)',
                    'TR5 100MVA 132/33kV (2ALATR5)',
                    'TR6 100MVA 132/33kV (2ALATR6)',
                ],
            },
            "Akoka 132kV": {
                "Transformer": [
                    'TR1 45MVA 132/33kV (3AKKTR1)',
                    'TR3 40MVA 132/33kV (3AKKTR3)',
                ],
            },
            "Oworonshoki 132kV": {
                "Transmission Line": [
                    'Ikeja West-Oworonshoki 132kV Line 1 (3KJW-WRK1)',
                    'Ikeja West-Oworonshoki 132kV Line 2 (3KJW-WRK2)',
                ],
            },
            "Amuwo-Odofin 132kV": {
                "Transformer": [
                    'TR3 60MVA 132/33kV (3JJJTR3)',
                    'TR4 60MVA 132/33kV (3JJJTR4)',
                ],
                "Transmission Line": [
                    'Akangba-Amuwo 132kV Line 1 (3AKG-AMW1)',
                    'Akangba-Amuwo/Apapa 132kV Line 2 (3AKG-AMW2)',
                ],
            },
            "Apapa-Road 132kV": {
                "Transmission Line": ['Akangba-Amuwo/Apapa 132kV Line 2 (3AKG-AMW2)'],
            },
        },
        "Akangba Sub-Region": {
            "Akangba 330kV": {
                "Transformer": [
                    'TR1 90MVA 330/132kV (2AKGTR1)',
                    'TR2 90MVA 330/132kV (2AKGTR2)',
                    'TR3 90MVA 330/132kV (2AKGTR3)',
                    'TR4 90MVA 330/132kV (2AKGTR4)',
                    'TR5 150MVA 330/132kV (2AKGTR5)',
                    'TR6 150MVA 330/132kV (2AKGTR6)',
                    'TR7 300MVA 330/132kV (2AKGTR7)',
                ],
                "Transmission Line": [
                    'Ikeja West-Akangba 330kV Line 1 (2KJW-AKG1)',
                    'Ikeja West-Akangba 330kV Line 2 (2KJW-AKG2)',
                ],
            },
            "Akangba 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3AKGTR1)',
                    'TR2 60MVA 132/33kV (3AKGTR2)',
                    'TR3 60MVA 132/33kV (3AKGTR3)',
                    'TR4 60MVA 132/33kV (3AKGTR4)',
                    'TR5 60MVA 132/33kV (3AKGTR5)',
                ],
                "Transmission Line": [
                    'Akangba-Isolo 132kV Line 1 (3AKG-SSL1)',
                    'Akangba-Isolo 132kV Line 2 (3AKG-SSL2)',
                    'Akangba-Ijora 132kV Line 1 (3AKG-JRA1)',
                    'Akangba-Ijora 132kV Line 2 (3AKG-JRA2)',
                    'Akangba-Amuwo 132kV Line 1 (3AKG-AMW1)',
                    'Akangba-Amuwo/Apapa 132kV Line 2 (3AKG-AMW2)',
                    'Akangba-Itire 132kV Line 1 (3AKG-TRE1)',
                    'Akangba-Itire 132kV Line 2 (3AKG-TRE2)',
                ],
            },
            "Ilupeju 132kV": {
                "Transmission Line": [
                    'Ikeja West-Ilupeju/Maryland 132kV Line 1 (3KJW-PJU-MRL1)',
                    'Ikeja West-Ilupeju/Maryland 132kV Line 2 (3KJW-PJU-MRL2)',
                    'Maryland-Ilupeju 132kV Line 1 (3MRL-LPJ1)',
                    'Maryland-Ilupeju 132kV Line 2 (3MRL-LPJ2)',
                ],
            },
            "Isolo 132kV": {
                "Transmission Line": [
                    'Akangba-Isolo 132kV Line 1 (3AKG-SSL1)',
                    'Akangba-Isolo 132kV Line 2 (3AKG-SSL2)',
                ],
            },
            "Itire 132kV": {
                "Transmission Line": [
                    'Akangba-Itire 132kV Line 1 (3AKG-TRE1)',
                    'Akangba-Itire 132kV Line 2 (3AKG-TRE2)',
                ],
            },
            "Ijora 132kV": {
                "Transmission Line": [
                    'Akangba-Ijora 132kV Line 1 (3AKG-JRA1)',
                    'Akangba-Ijora 132kV Line 2 (3AKG-JRA2)',
                ],
            },
            "Ojo 132kV": {
            },
            "Ilashe 132kV": {
            },
        },
        "Egbin Sub-Region": {
            "Egbin 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132/33kV (IBTR1)',
                    'TR2 150MVA 330/132/33kV (IBTR2)',
                ],
                "Transmission Line": [
                    'Egbin-Oke Aro 330kV Line 1 (3EGN-KER1)',
                    'Egbin-Oke Aro 330kV Line 2 (3EGN-KER2)',
                    'Egbin-Ikeja West 330kV Line 1 (3EGN-KJA1)',
                    'Benin-Egbin 330kV Line 1 (3BEN-EGB1)',
                    'Egbin-Aja 330kV Line 1 (3EGN-AJA1)',
                    'Egbin-Aja 330kV Line 2 (3EGN-AJA2)',
                ],
            },
            "Egbin 132kV": {
                "Transmission Line": [
                    'Egbin-Ikorodu 132kV Line 1 (3GBN-KRD1)',
                    'Egbin-Ikorodu 132kV Line 2 (3GBN-KRD2)',
                ],
            },
            "Ikorodu 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV',
                    'TR2 60MVA 132/33kV',
                    'TR3 100MVA 132/33kV',
                    'TR4 60MVA 132/33kV',
                ],
                "Transmission Line": [
                    'Egbin-Ikorodu 132kV Line 1 (3GBN-KRD1)',
                    'Egbin-Ikorodu 132kV Line 2 (3GBN-KRD2)',
                    'Ikorodu-Shagamu 132kV Line 1 (3KRD-SGM1)',
                    'Ikorodu-Odogunyan-Shagamu 132kV Line 2 (3KRD-DGY-SGM2)',
                ],
            },
            "Odogunyan 132kV": {
                "Transmission Line": ['Ikorodu-Odogunyan-Shagamu 132kV Line 2 (3KRD-DGY-SGM2)'],
            },
        },
        "Ikeja-West Sub-Region": {
            "Ikeja West 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (KJWTR1)',
                    'TR2 150MVA 330/132kV (KJWTR2)',
                    'TR3 150MVA 330/132kV (KJWTR3)',
                    'TR4 150MVA 330/132kV (KJWTR4)',
                    'TR5 150MVA 330/132kV (KJWTR5)',
                    'TR6 300MVA 330/132kV (KJWTR6)',
                ],
                "Transmission Line": [
                    'Ikeja West-Oshogbo 330kV (2KJW-SHG)',
                    'Ikeja West-Olorunsogo 330kV (2KJW-RSG)',
                    'Ikeja West-Akangba 330kV Line 1 (2KJW-AKG1)',
                    'Ikeja West-Akangba 330kV Line 2 (2KJW-AKG2)',
                    'Ikeja West-Omotosho 330kV (2KJW-MTS)',
                    'Ikeja West-Egbin 330kV (2KJW-EGN)',
                    'Ikeja West-Oke Aro 330kV Line 1 (2KJW-KER1)',
                    'Ikeja West-Oke Aro 330kV Line 2 (2KJW-KER2)',
                    'Ikeja West-Sakete 330kV (2KJW-BSK)',
                ],
                "Reactor": [
                    '75Mvar Reactor 1 (2KJWRX1)',
                    '75Mvar Reactor 2 (2KJWRX2)',
                ],
            },
            "Alausa 132kV": {
                "Transmission Line": ['Ikeja West-Alausa 132kV'],
            },
            "Ogba 132kV": {
            },
            "Alimosho 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (AMSTR1)',
                    'TR2 100MVA 132/33kV (AMSTR2)',
                    'TR3 100MVA 132/33kV (AMSTR3)',
                ],
                "Transmission Line": [
                    'Ikeja West-Alimosho 132kV Line 1 (3KJW-AMS1)',
                    'Ikeja West-Alimosho 132kV Line 2 (3KJW-AMS2)',
                ],
            },
            "Ejigbo 132kV": {
                "Transmission Line": [
                    'Ikeja West-Ejigbo 132kV Line 1 (3KJW-EJB1)',
                    'Ikeja West-Ejigbo 132kV Line 2 (3KJW-EJB2)',
                ],
            },
            "Agbara 132kV": {
                "Transmission Line": [
                    'Ikeja West-Agbara 132kV Line 1 (3KJW-AGR1)',
                    'Ikeja West-Agbara 132kV Line 2 (3KJW-AGR2)',
                ],
            },
        },
        "Papalanto Sub-Region": {
            "Olorunsogo 330kV": {
                "Transmission Line": [
                    'Olorunsogo-Ikeja West 330kV (2KJW-RSG)',
                    'Olorunsogo-Ayede 330kV (2RSG-YDE)',
                ],
            },
            "Otta 132kV": {
                "Transformer": [
                    'TR1 100MVA 132/33kV (3TTATR1)',
                    'TR2 60MVA 132/33kV (3TTATR2)',
                    'TR3 100MVA 132/33kV (3TTATR3)',
                    'TR4 60MVA 132/33kV (3TTATR4)',
                    'TR5 MOBITRA 40MVA (3TTATR5)',
                ],
                "Transmission Line": [
                    'Ikeja West-Otta 132kV Line 1 (3KJW-TTA1)',
                    'Ikeja West-Otta 132kV Line 2 (3KJW-TTA2)',
                    'Otta-Papalanto 132kV Line 1 (3TTA-PPT1)',
                    'Otta-Papalanto 132kV Line 2 (3TTA-PPT2)',
                ],
            },
            "Papalanto 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3PPTTR1)',
                    'TR2 30MVA 132/33kV (3PPTTR2)',
                    'TR3 30MVA 132/33kV (3PPTTR3)',
                ],
                "Transmission Line": [
                    'Otta-Papalanto 132kV Line 1 (3TTA-PPT1)',
                    'Otta-Papalanto 132kV Line 2 (3TTA-PPT2)',
                    'Papalanto-Abeokuta 132kV Line 1 (3PPT-ABK1)',
                    'Papalanto-Abeokuta 132kV Line 2 (3PPT-ABK2)',
                ],
            },
            "Abeokuta 132kV": {
                "Transmission Line": [
                    'Papalanto-Abeokuta 132kV Line 1 (3PPT-ABK1)',
                    'Papalanto-Abeokuta 132kV Line 2 (3PPT-ABK2)',
                ],
            },
            "New Abeokuta 132kV": {
            },
        },
    },

    # ===================== OSOGBO REGION =====================
    "Osogbo": {
        "Osogbo Sub-region": {
            "Oshogbo 330kV": {
                "Transformer": [
                    'TR1 90MVA 330/132kV (2SGBTR1)',
                    'TR3 150MVA 330/132kV (2SGBTR3)',
                    'TR4 150MVA 330/132kV (2SGBTR4)',
                ],
                "Transmission Line": [
                    'Jebba-Osogbo 330kV Line 1 (2JEB-SGB1)',
                    'Jebba-Osogbo 330kV Line 2 (2JEB-SGB2)',
                    'Osogbo-Ganmo 330kV Line 1 (2SGB-GNM1)',
                    'Ihovbor-Osogbo 330kV Line 1 (2HVR-SGB1)',
                    'Osogbo-Ikeja West 330kV Line 1 (2SGB-KJW1)',
                    'Osogbo-Ayede 330kV Line 1 (2SGB-YDE1)',
                ],
                "Reactor": ['75Mvar Reactor (2SGBRX1)'],
            },
            "Oshogbo 132kV": {
                "Transformer": [
                    'TR2 45/60MVA 132/33kV (3SGBTR2)',
                    'TR3 60MVA 132/33kV (3SGBTR3)',
                    'TR4 60MVA 132/33kV (3SGBTR4)',
                ],
                "Transmission Line": [
                    'Osogbo-Offa-Omuaran-Ganmo 132kV (3SGB-FFA-MRN-GNM)',
                    'Osogbo-Akure 132kV (3SGB-AKR)',
                    'Osogbo-Ilesa-Ife 132kV (3SGB-LES-FFE)',
                    'Osogbo-Iwo 132kV (3SGB-WWD)',
                ],
            },
            "Ile-Ife 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3FFETR1)',
                    'TR2 30MVA 132/33kV (3FFETR2)',
                ],
                "Transmission Line": ['Ife-Ondo 132kV (3FFE-NND)'],
            },
            "Ilesha 132kV": {
                "Transformer": [
                    'TR1 40/30MVA 132/33kV (3LESTR1)',
                    'TR2 40/30MVA 132/33kV (3LESTR2)',
                ],
            },
            "Offa 132kV": {
                "Transformer": ['TR1 40MVA 132/33kV (3FFATR1)'],
                "Transmission Line": ['Osogbo-Offa-Omuaran-Ganmo 132kV (3SGB-FFA-MRN-GNM)'],
            },
            "Iwo 132kV": {
                "Transformer": ['TR1 28/40MVA 132/33kV (3WWDTR1)'],
                "Transmission Line": [
                    'Osogbo-Iwo 132kV (3SGB-WWD)',
                    'Ayede-UI-Ibadan North-Iwo 132kV (3YDE-UIB-BDN-WWD)',
                ],
            },
        },
        "Ayede Sub-region": {
            "Ayede 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2YDETR1)',
                    'TR2 150MVA 330/132kV (2YDETR2)',
                    'TR3 150MVA 330/132kV (2YDETR3)',
                    'TR4 150MVA 330/132kV (2YDETR4)',
                ],
                "Transmission Line": [
                    'Olorunsogo-Ayede 330kV (2RSG-YDE)',
                    'Osogbo-Ayede 330kV Line 1 (2SGB-YDE1)',
                ],
            },
            "Ayede 132kV": {
                "Transformer": [
                    'TR1 100MVA 132/33kV (3YDETR1)',
                    'TR2 60MVA 132/33kV (3YDETR2)',
                    'TR3 60MVA 132/33kV (3YDETR3)',
                ],
                "Transmission Line": [
                    'Ayede-UI-Ibadan North-Iwo 132kV (3YDE-UIB-BDN-WWD)',
                    'Ayede-Jericho 132kV (3YDE-JRC)',
                    'Ayede-McPherson-Saapade-Shagamu 132kV (3YDE-MPC-SPD-SGM)',
                ],
            },
            "Ibadan-North 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3BDNTR1)',
                    'TR2 60MVA 132/33kV (3BDNTR2)',
                ],
            },
            "Jericho 132kV": {
                "Transformer": ['TR2 40MVA 132/33kV (3JRCTR2)'],
                "Transmission Line": ['Ayede-Jericho 132kV (3YDE-JRC)'],
            },
            "Shagamu 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3SGMTR2)',
                    'TR2 30MVA 132/33kV (3SGMTR4)',
                    'TR4 60MVA 132/33kV (3SGMTR3)',
                ],
                "Transmission Line": [
                    'Shagamu-Ijebu Ode 132kV (3SGM-JBD)',
                    'Ikorodu-Shagamu 132kV Line 1 (3KRD-SGM1)',
                    'Ikorodu-Odogunyan-Shagamu 132kV Line 2 (3KRD-DGY-SGM2)',
                ],
            },
            "Ijebu-Ode 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3JBDTR2)',
                    'TR2 30MVA 132/33kV (3JBDTR3)',
                ],
                "Transmission Line": ['Shagamu-Ijebu Ode 132kV (3SGM-JBD)'],
            },
            "Iseyin 132kV": {
                "Transformer": [
                    'TR1 45/30MVA 132/33kV (3SYNTR1)',
                    'TR2 30MVA 132/33kV (3SYNTR2)',
                ],
            },
            "Mcpherson 132kV": {
                "Transformer": ['TR1 28/40MVA 132/33kV (3MPCTR1)'],
                "Transmission Line": ['Ayede-McPherson-Saapade-Shagamu 132kV (3YDE-MPC-SPD-SGM)'],
            },
            "Oyo 132kV": {
            },
            "UI 132kV": {
                "Transformer": ['TR1 63MVA 132/33kV (3UIBTR1)'],
            },
            "Saapade 132kV": {
                "Transformer": ['TR1 63MVA 132/33kV (3SPDTR1)'],
                "Transmission Line": ['Ayede-McPherson-Saapade-Shagamu 132kV (3YDE-MPC-SPD-SGM)'],
            },
        },
        "Ganmo Sub-region": {
            "Ganmo 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2GNMTR1)',
                    'TR2 150MVA 330/132kV (2GNMTR2)',
                    'TR3 300MVA 330/132kV (2GNMTR3)',
                ],
                "Transmission Line": ['Osogbo-Ganmo 330kV Line 1 (2SGB-GNM1)'],
            },
            "Ganmo 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3GNMTR1)',
                    'TR2 60MVA 132/33kV (3GNMTR2)',
                ],
                "Transmission Line": [
                    'Ganmo-Ilorin 132kV (3GNM-LRN)',
                    'Osogbo-Offa-Omuaran-Ganmo 132kV (3SGB-FFA-MRN-GNM)',
                ],
            },
            "Ilorin 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3LRNTR2)',
                    'TR2 45/30MVA 132/33kV (3LRNTR3)',
                    'TR3 100MVA 132/33kV (3LRNTR1)',
                ],
                "Transmission Line": ['Ganmo-Ilorin 132kV (3GNM-LRN)'],
            },
            "Omu-Aran 132kV": {
                "Transformer": ['TR1 30MVA 132/33kV (3MRNTR1)'],
                "Transmission Line": ['Osogbo-Offa-Omuaran-Ganmo 132kV (3SGB-FFA-MRN-GNM)'],
            },
        },
        "Akure W/C": {
            "Akure 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3AKRTR3)',
                    'TR3 30MVA 132/33kV (3AKRTR1)',
                    'TR4 60MVA 132/33kV (3AKRTR2)',
                ],
                "Transmission Line": [
                    'Osogbo-Akure 132kV (3SGB-AKR)',
                    'Akure-Ado Ekiti 132kV (3AKR-ADK)',
                ],
            },
            "Ado Ekiti 132kV": {
                "Transformer": [
                    'TR1 40/30MVA 132/33kV (3ADKTR1)',
                    'TR2 40/30MVA 132/33kV (3ADKTR2)',
                    'TR3 66/60MVA 132/33kV (3ADKTR3)',
                ],
                "Transmission Line": ['Akure-Ado Ekiti 132kV (3AKR-ADK)'],
            },
        },
    },

    # ===================== PORT-HARCOURT REGION =====================
    "Port-Harcourt": {
        "Port Harcourt Sub-region": {
            "PH Main 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3PHMTR1)',
                    'TR2 60MVA 132/33kV (3PHMTR2)',
                    'TR3 60MVA 132/33kV (3PHMTR3)',
                    'TR4 125MVA 132/33kV (3PHMTR4)',
                ],
                "Transmission Line": [
                    'Afam IPP-PH Main-PH Town 132kV Line 1 (3AIP-PHM-PHT1)',
                    'Afam IPP-PH Main-PH Town 132kV Line 2 (3AIP-PHM-PHT2)',
                    'PH Main-Rumuosi 132kV Line 1 (3PHM-RUM1)',
                    'PH Main-Trans Amadi 132kV Line 1 (3PHM-TAD1)',
                    'PH Main-Trans Amadi 132kV Line 2 (3PHM-TAD2)',
                ],
            },
            "PH Town 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3PHTTR1)',
                    'TR2 30/45MVA 132/33kV (3PHTTR2)',
                    'TR3 30MVA 132/33kV (3PHTTR3)',
                    'TR4 125MVA 132/33kV (3PHTTR4)',
                ],
                "Transmission Line": [
                    'Afam IPP-PH Main-PH Town 132kV Line 1 (3AIP-PHM-PHT1)',
                    'Afam IPP-PH Main-PH Town 132kV Line 2 (3AIP-PHM-PHT2)',
                ],
            },
            "Rumuosi 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3RUMTR1)',
                    'TR2 60MVA 132/33kV (3RUMTR2)',
                ],
                "Transmission Line": [
                    'PH Main-Rumuosi 132kV Line 1 (3PHM-RUM1)',
                    'PH Main-Rumuosi 132kV Line 2 (3PHM-RUM2)',
                    'Rumuosi-Makurdi 132kV Line 1 (3RUM-MKU1)',
                    'Rumuosi-Makurdi 132kV Line 2 (3RUM-MKU2)',
                ],
            },
            "Elelenwo 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3ELNTR1)',
                    'TR2 60MVA 132/33kV (3ELNTR2)',
                ],
                "Transmission Line": [
                    'Afam IPP-Elelenwo 132kV Line 1 (3AIP-ELN1)',
                    'Afam IPP-Elelenwo 132kV Line 2 (3AIP-ELN2)',
                ],
            },
            "Ahoada 132kV": {
                "Transformer": [
                    'TR1 30/40MVA 132/33kV (3AHDTR1)',
                    'TR2 30/40MVA 132/33kV (3AHDTR2)',
                ],
                "Transmission Line": [
                    'Owerri-Ahoada 132kV Line 1 (3WER-AHD1)',
                    'Owerri-Ahoada 132kV Line 2 (3WER-AHD2)',
                ],
            },
            "Gbarain 132kV": {
                "Transformer": ['TR2 60MVA 132/33kV (3GBNTR1)'],
                "Transmission Line": [
                    'Gbarain-Yenagoa 132kV Line 1 (3GBN-YEN1)',
                    'Gbarain-Yenagoa 132kV Line 2 (3GBN-YEN2)',
                    'Ahoada-Gbarain 132kV Line 1 (3AHD-GBN1)',
                    'Ahoada-Gbarain 132kV Line 2 (3AHD-GBN2)',
                ],
            },
            "Yenagoa 132kV": {
                "Transformer": [
                    'TR1 90/95MVA 132/33kV (3YENTR1)',
                    'TR2 30/40MVA 132/33kV (3YENTR2)',
                ],
                "Transmission Line": [
                    'Gbarain-Yenagoa 132kV Line 1 (3GBN-YEN1)',
                    'Gbarain-Yenagoa 132kV Line 2 (3GBN-YEN2)',
                ],
            },
        },
        "Uyo W/C": {
            "Ikot-Ekpene 330kV": {
                "Transmission Line": [
                    'Odukpani-Ikot Ekpene 330kV Line 1 (2DKP-KPE1)',
                    'Odukpani-Ikot Ekpene 330kV Line 2 (2DKP-KPE2)',
                    'Afam-Ikot Ekpene 330kV Line 1 (2AFM-KPE1)',
                    'Afam-Ikot Ekpene 330kV Line 2 (2AFM-KPE2)',
                    'Alaoji-Ikot Ekpene 330kV Line 1 (2ALJ-KPE1)',
                    'Alaoji-Ikot Ekpene 330kV Line 2 (2ALJ-KPE2)',
                    'Ikot Ekpene-Ugwuaji 330kV Line 1 (2KPE-UGW1)',
                    'Ikot Ekpene-Ugwuaji 330kV Line 2 (2KPE-UGW2)',
                    'Ikot Ekpene-Ugwuaji 330kV Line 3 (2KPE-UGW3)',
                    'Ikot Ekpene-Ugwuaji 330kV Line 4 (2KPE-UGW4)',
                ],
            },
            "Itu 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3TTUTR1)',
                    'TR2 75MVA 132/33kV (3TTUTR2)',
                ],
                "Transmission Line": [
                    'Aba-Itu 132kV Line 1 (3ABA-TTU1)',
                    'Itu-Uyo 132kV Line 1 (3TTU-UYY1)',
                    'Itu-Adiabor 132kV Line 1 (3TTU-ADB1)',
                ],
            },
            "Uyo 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3UYYTR1)',
                    'TR2 60MVA 132/33kV (3UYYTR2)',
                    'TR3 60MVA 132/33kV (3UYYTR3)',
                ],
                "Transmission Line": [
                    'Itu-Uyo 132kV Line 1 (3TTU-UYY1)',
                    'Uyo-Eket 132kV Line 1 (3UYY-EKT1)',
                ],
            },
            "Eket 132kV": {
                "Transformer": [
                    'TR1 45MVA 132/33kV (3EKTTR1)',
                    'TR2 60MVA 132/33kV (3EKTTR2)',
                ],
                "Transmission Line": [
                    'Uyo-Eket 132kV Line 1 (3UYY-EKT1)',
                    'Bonny-Eket 132kV Line 1 (3BOM-EKT1)',
                    'Bonny-Ekim-Eket 132kV Line 1 (3BOM-EKM-EKT1)',
                ],
            },
            "Ekim 132kV": {
                "Transformer": ['TR1 60MVA 132/33kV (3EKMTR1)'],
                "Transmission Line": ['Bonny-Ekim-Eket 132kV Line 1 (3BOM-EKM-EKT1)'],
            },
        },
        "Calabar Sub-region": {
            "Adiabor 330kV": {
                "Transformer": [
                    'TR1 150/165MVA 330/132kV (2ADBTR1)',
                    'TR2 150MVA 330/132kV (2ADBTR2)',
                ],
                "Transmission Line": [
                    'Odukpani-Adiabor 330kV Line 1 (2DKP-ADB1)',
                    'Odukpani-Adiabor 330kV Line 2 (2DKP-ADB2)',
                    'Adiabor-Calabar 132kV Line 1 (3ADB-CAL1)',
                    'Adiabor-Calabar 132kV Line 2 (3ADB-CAL2)',
                ],
                "Reactor": ['Reactor (2ADBRX1)'],
            },
            "Adiabor 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3ADBTR1)',
                    'TR2 60MVA 132/33kV (3ADBTR2)',
                ],
            },
            "Odukpani 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2DKPTR1)',
                    'TR2 60MVA 330/132kV (2DKPTR2)',
                ],
                "Transmission Line": [
                    'Odukpani-Ikot Ekpene 330kV Line 1 (2DKP-KPE1)',
                    'Odukpani-Ikot Ekpene 330kV Line 2 (2DKP-KPE2)',
                    'Odukpani-Adiabor 330kV Line 1 (2DKP-ADB1)',
                    'Odukpani-Adiabor 330kV Line 2 (2DKP-ADB2)',
                ],
            },
            "Calabar 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3CALTR1)',
                    'TR2 60MVA 132/33kV (3CALTR2)',
                    'TR3 60MVA 132/33kV (3CALTR3)',
                    'TR4 60MVA 132/33kV (3CALTR4)',
                ],
                "Transmission Line": [
                    'Adiabor-Calabar 132kV Line 1 (3ADB-CAL1)',
                    'Adiabor-Calabar 132kV Line 2 (3ADB-CAL2)',
                ],
            },
        },
        "Afam Sub-region": {
            "Afam 132kV": {
                "Transformer": [
                    'TR1 45MVA 132/33kV (3AFMTR1)',
                    'TR2 64MVA 132/33kV (3AFMTR2)',
                ],
                "Transmission Line": [
                    'Afam-Afam IPP 132kV Line 1 (3AFM-AIP1)',
                    'Afam-Afam IPP 132kV Line 2 (3AFM-AIP2)',
                    'Afam-Alaoji 132kV Line 1 (3AFM-ALJ1)',
                    'Afam-Alaoji 132kV Line 2 (3AFM-ALJ2)',
                ],
            },
            "Afam 4 330kV": {
                "Transformer": [
                    'TR1 162MVA 330/132kV (2AFM4TR1)',
                    'TR2 150MVA 330/132kV (2AFM4TR2)',
                ],
                "Transmission Line": [
                    'Afam-Alaoji 330kV Line 1 (2AFM-ALJ1)',
                    'Afam-Alaoji 330kV Line 2 (2AFM-ALJ2)',
                    'Afam-Ikot Ekpene 330kV Line 1 (2AFM-NNE1)',
                    'Afam-Ikot Ekpene 330kV Line 2 (2AFM-NNE2)',
                ],
            },
            "Afam 6 132kV": {
                "Transmission Line": [
                    'Afam 6-Ikot Ekpene 132kV Line 1 (3AFM-KPE1)',
                    'Afam 6-Ikot Ekpene 132kV Line 2 (3AFM-KPE2)',
                ],
            },
        },
        "Aba Sub-region": {
            "Alaoji 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2ALJTR1)',
                    'TR2 150MVA 330/132kV (2ALJTR2)',
                    'TR3 150MVA 330/132kV (2ALJTR3)',
                    'TR4 300MVA 330/132kV (2ALJTR4)',
                ],
                "Transmission Line": [
                    'Afam-Alaoji 330kV Line 1 (2AFM-ALJ1)',
                    'Afam-Alaoji 330kV Line 2 (2AFM-ALJ2)',
                    'Alaoji-Onitsha 330kV Line 1 (2ALJ-NSH1)',
                    'Alaoji-Ikot Ekpene 330kV Line 1 (2ALJ-KPE1)',
                    'Alaoji-Ikot Ekpene 330kV Line 2 (2ALJ-KPE2)',
                    'Alaoji NIPP-Alaoji 330kV Line 1 (2ALN-ALJ1)',
                    'Alaoji NIPP-Alaoji 330kV Line 2 (2ALN-ALJ2)',
                ],
                "Reactor": ['Reactor (2ALJRX1)'],
            },
            "Alaoji 132kV": {
                "Transmission Line": [
                    'Alaoji-Afam 132kV Line 1 (3ALJ-AFM1)',
                    'Alaoji-Afam 132kV Line 2 (3ALJ-AFM2)',
                    'Alaoji-Aba 132kV Line 1 (3ALJ-ABA1)',
                    'Alaoji-Aba 132kV Line 2 (3ALJ-ABA2)',
                    'Alaoji-Owerri 132kV Line 1 (3ALJ-WER1)',
                    'Alaoji-Owerri 132kV Line 2 (3ALJ-WER2)',
                    'Alaoji-Umuahia 132kV Line 1 (3ALJ-UMA1)',
                    'Alaoji-Umuahia 132kV Line 2 (3ALJ-UMA2)',
                ],
            },
            "Umuahia 132kV": {
                "Transformer": [
                    'TR1 30/40MVA 132/33kV (3UMATR1)',
                    'TR2 30/40MVA 132/33kV (3UMATR2)',
                    'TR3 MOBITRA 38/40MVA (3UMATR3)',
                ],
                "Transmission Line": [
                    'Alaoji-Umuahia 132kV Line 1 (3ALJ-UMA1)',
                    'Alaoji-Umuahia 132kV Line 2 (3ALJ-UMA2)',
                ],
            },
            "Aba 132kV": {
                "Transformer": [
                    'TR1 7.5MVA 132/33kV (3ABATR1)',
                    'TR2 60MVA 132/33kV (3ABATR2)',
                    'TR3 60MVA 132/33kV (3ABATR3)',
                    'TR4 60MVA 132/33kV (3ABATR4)',
                    'TR5 75MVA 132/33kV (3ABATR5)',
                ],
                "Transmission Line": [
                    'Alaoji-Aba 132kV Line 1 (3ALJ-ABA1)',
                    'Alaoji-Aba 132kV Line 2 (3ALJ-ABA2)',
                    'Aba-Itu 132kV Line 1 (3ABA-TTU1)',
                ],
            },
        },
        "Owerri W/C": {
            "Owerri 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3WERTR1)',
                    'TR2 60MVA 132/33kV (3WERTR2)',
                    'TR3 MOBITRA 40MVA (3WERTR3)',
                ],
                "Transmission Line": [
                    'Alaoji-Owerri 132kV Line 1 (3ALJ-WER1)',
                    'Alaoji-Owerri 132kV Line 2 (3ALJ-WER2)',
                    'Owerri-Ahoada 132kV Line 1 (3WER-AHD1)',
                    'Owerri-Ahoada 132kV Line 2 (3WER-AHD2)',
                ],
            },
        },
    },

    # ===================== SHIRORO REGION =====================
    "Shiroro": {
        "Shiroro Sub-region": {
            "Shiroro 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132/33kV (2SHRTR1)',
                    'TR2 150MVA 330/132/33kV (2SHRTR2)',
                ],
                "Transmission Line": [
                    'Shiroro-Mando 330kV Line 1 (2SHR-MND1)',
                    'Shiroro-Mando 330kV Line 2 (2SHR-MND2)',
                    'Shiroro-Mararaba 330kV Line 1 (2SHR-MRB1)',
                    'Shiroro-Mararaba 330kV Line 2 (2SHR-MRB2)',
                    'Shiroro-Katampe 330kV Line 1 (2SHR-KTP1)',
                    'Shiroro-Gwagwalada 330kV Line 1 (2SHR-GWA1)',
                ],
            },
            "Shiroro 132kV": {
                "Transmission Line": [
                    'Shiroro-Minna 132kV Line 1 (3SHR-MNA1)',
                    'Shiroro-Minna 132kV Line 2 (3SHR-MNA2)',
                    'Shiroro-Tegina-Kontagora-Yauri 132kV (3SHR-TEG-KNT-YAU)',
                ],
            },
            "Shiroro II TS 132kV": {
                "Transformer": ['TR1 30MVA 132/33kV (3SHRTR1)'],
                "Transmission Line": ['Shiroro-Shiroro II-Minna 132kV Line 2 (3SHR-SHR2-MNA2)'],
            },
            "Minna 132kV": {
                "Transformer": [
                    'TR1 60MVA 132/33kV (3MNATR1)',
                    'TR2 30MVA 132/33kV (3MNATR2)',
                    'TR5 60MVA 132/33kV (3MNATR5)',
                ],
                "Transmission Line": [
                    'Shiroro-Minna 132kV Line 1 (3SHR-MNA1)',
                    'Minna-Bida 132kV Line 1 (3MNA-BDA1)',
                    'Minna-Shiroro 132kV Line 2 (3MNA-SHR2)',
                    'Minna-Suleja 132kV Line 1 (3MNA-SUL1)',
                    'Minna-Suleja 132kV Line 2 (3MNA-SUL2)',
                ],
            },
            "Zungeru 330kV": {
                "Transformer": [
                    'TR1 150MVA 330/132kV (2ZGUTR1)',
                    'TR2 150MVA 330/132kV (2ZGUTR2)',
                ],
                "Transmission Line": [
                    'Zungeru-Mararaba 330kV Line 1 (2ZUN-MRB1)',
                    'Zungeru-Mararaba 330kV Line 2 (2ZUN-MRB2)',
                ],
            },
            "Zungeru 132kV": {
                "Transformer": ['TR3 30MVA 132/33kV (3ZGUTR3)'],
                "Transmission Line": [
                    'Zungeru-Tegina 132kV Line 1 (3ZGU-TEG1)',
                    'Zungeru-Tegina 132kV Line 2 (3ZGU-TEG2)',
                ],
            },
            "Mararaba TS 132kV": {
                "Transmission Line": [
                    'Mararaba-Shiroro 330kV Line 1 (2SHR-MRB1)',
                    'Mararaba-Shiroro 330kV Line 2 (2SHR-MRB2)',
                    'Mararaba-Jebba 330kV Line 1 (2JEB-MRB1)',
                    'Mararaba-Jebba 330kV Line 2 (2JEB-MRB2)',
                    'Mararaba-Zungeru 330kV Line 1 (2ZUN-MRB1)',
                    'Mararaba-Zungeru 330kV Line 2 (2ZUN-MRB2)',
                ],
            },
        },
        "Kainji W/C": {
            "Kainji 330kV": {
                "Transformer": ['TR1 150MVA 330/132kV (2FAKTR1)'],
                "Transmission Line": [
                    'Kainji-Fakum 330kV Line 1 (2KNJ-FAK1)',
                    'Birnin Kebbi-Kainji 330kV Line 1 (2BRK-KNJ1)',
                ],
            },
            "Kainji 132kV": {
                "Transmission Line": [
                    'Fakum-Dogongeri 132kV Line 1 (3FAK-DGR1)',
                    'Fakum-Dogongeri 132kV Line 2 (3FAK-DGR2)',
                ],
            },
            "Kainji II TS 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3DGNTR1)',
                    'TR2 40MVA 132/33kV (3DGNTR2)',
                ],
                "Transmission Line": [
                    'Dogongeri-Fakum 132kV Line 1 (3DGR-FAK1)',
                    'Dogongeri-Fakum 132kV Line 2 (3DGR-FAK2)',
                ],
            },
        },
        "Kontagora W/C": {
            "Tegina 132kV": {
                "Transformer": ['TR1 30MVA 132/33kV (3TEGTR1)'],
                "Transmission Line": [
                    'Shiroro-Tegina-Yauri 132kV (3SHR-TEG-YAU2)',
                    'Tegina-Zungeru 132kV Line 1 (3TEG-ZGR1)',
                    'Tegina-Zungeru 132kV Line 2 (3TEG-ZGR2)',
                ],
            },
            "Kontagora 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3KNTTR1)',
                    'TR2 60MVA 132/33kV (3KNTTR2)',
                ],
                "Transmission Line": [
                    'Shiroro-Tegina-Kontagora-Yauri 132kV',
                    'Kontagora-Yauri 132kV Line 1 (3KNT-YAU1)',
                ],
            },
            "Yauri 132kV": {
                "Transformer": [
                    'TR1 40MVA 132/33kV (3YAUTR1)',
                    'TR2 40MVA 132/33kV (3YAUTR2)',
                ],
                "Transmission Line": ['Kontagora-Yauri 132kV Line 1 (3KNT-YAU1)'],
            },
        },
        "Jebba Sub-region": {
            "Jebba 330kV": {
                "Transformer": ['TR1 80MVA 330/132kV (2JEBTR1)'],
                "Transmission Line": [
                    'Jebba-Mararaba 330kV Line 1 (2JEB-MRB1)',
                    'Jebba-Mararaba 330kV Line 2 (2JEB-MRB2)',
                    'Jebba-Ganmo 330kV Line 1 (2JEB-GAM1)',
                    'Jebba-Osogbo 330kV Line 1 (2JEB-SGB1)',
                    'Jebba-Osogbo 330kV Line 2 (2JEB-SGB2)',
                    'Jebba-Jebba GS 330kV Line 1 (2JEB-JEG1)',
                    'Jebba-Jebba GS 330kV Line 2 (2JEB-JEG2)',
                    'Kainji-Jebba 330kV Line 1 (1KNJ-JEB1)',
                    'Kainji-Jebba 330kV Line 2 (1KNJ-JEB2)',
                ],
                "Reactor": [
                    '75Mvar Reactor 1 (2JEBREA1)',
                    '75Mvar Reactor 2 (2JEBREA2)',
                ],
            },
            "Jebba 132kV": {
                "Transformer": [
                    'TR2 30MVA 132/33kV (3JEBTR2)',
                    'TR3 63MVA 132/33kV (3JEBTR3)',
                ],
            },
            "Bida 132kV": {
                "Transformer": [
                    'TR1 30MVA 132/33kV (3BDATR1)',
                    'TR2 30MVA 132/33kV (3BDATR2)',
                    'TR3 60MVA 132/33kV (3BDATR3)',
                ],
                "Transmission Line": ['Bida-Minna 132kV Line 1 (3BDA-MNA1)'],
            },
        },
    },
}


def get_substations_for(region, subregion):
    return sorted(SUBSTATION_EQUIPMENT.get(region, {}).get(subregion, {}).keys())


def get_equipment_types_for(region, subregion, substation):
    equip = SUBSTATION_EQUIPMENT.get(region, {}).get(subregion, {}).get(substation, {})
    return sorted(equip.keys())


def get_equipment_list(region, subregion, substation, equip_type):
    return SUBSTATION_EQUIPMENT.get(region, {}).get(subregion, {}).get(substation, {}).get(equip_type, [])
