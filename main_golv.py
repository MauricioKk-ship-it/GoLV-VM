#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from golv import GoLVSetup, VMType, CommandSecurityLevel, SecurityError

def main():
    print("🚀 Initialisation du SDK GoLV...")

    # ---------- INITIALISATION ----------
    setup = GoLVSetup()
    print("SDK Setup:", setup)

    client = setup.get_client()
    print("Client OK:", client)

    # ---------- CRÉATION DE VM ----------
    vm_config = setup.create_vm_config(
        name="test-vm",
        vm_type=VMType.PYTHON_DEV
    )
    print("VMConfig:", vm_config)

    try:
        vm_data = client.create_vm(vm_config)
        vm_id = vm_data.get("vm_id")
        print(f"✅ VM créée avec ID: {vm_id}")
    except Exception as e:
        print(f"Erreur création VM: {e}")
        vm_id = None

    # ---------- CRÉATION AGENT ----------
    agent = setup.create_agent(
        vm_config=vm_config,
        allowed_commands=["echo", "python", "git"],
        max_command_length=100
    )
    print("Agent GoLV créé:", agent)

    # ---------- TEST COMMANDE ECHO ----------
    try:
        result = agent.execute("echo 'Hello GoLV'")
        print("Commande echo output:", result.output)
    except SecurityError as se:
        print("Erreur sécurité:", se)

    # ---------- TEST COMMANDE PYTHON ----------
    python_code = "print('Hello from Python inside VM')"
    result = agent.execute_python(python_code)
    print("Commande Python output:", result.output)

    # ---------- TEST COMMANDE INTERDITE ----------
    try:
        agent.execute("rm -rf /")  # devrait déclencher SecurityError
    except SecurityError as se:
        print("SecurityError détectée comme attendu:", se)

    # ---------- TEST STATUT VM ----------
    if vm_id:
        status = agent.get_status()
        print("Statut VM:", status)

    # ---------- TEST COMMANDE PREDEFINIE ----------
    try:
        predef_result = agent.predefined("list_files")
        print("Commande prédéfinie output:", predef_result.output)
    except Exception as e:
        print("Erreur commande prédéfinie:", e)

    print("✅ Tous les tests sont terminés.")

if __name__ == "__main__":
    main()
