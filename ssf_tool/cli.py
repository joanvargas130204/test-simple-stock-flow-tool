import argparse
import sys
from .client import ApiClient
from .sample_data import SAMPLE_PRODUCTS

def cmd_seed(args):
    print(f"[*] Conectando a {args.url} como {args.admin_user}...")
    client = ApiClient(args.url)
    try:
        client.login(args.admin_user, args.admin_password)
        print("[+] Autenticado exitosamente como Administrador.")
    except Exception as e:
        print(f"[-] Error al autenticar: {e}")
        sys.exit(1)

    # 1. Fetch categories to resolve IDs
    cats = client.get_categories()
    cat_map = {c["name"].lower(): c["id"] for c in cats}
    print(f"[+] Categorías detectadas en backend: {len(cats)}")

    # 2. Seed products
    created_product_ids = []
    print(f"[*] Sembrando {len(SAMPLE_PRODUCTS)} productos...")
    for p in SAMPLE_PRODUCTS:
        cat_id = cat_map.get(p["category"].lower())
        if not cat_id:
            print(f"[-] Categoría '{p['category']}' no encontrada. Usando General.")
            cat_id = cat_map.get("general", list(cat_map.values())[0])
        try:
            pid = client.create_product(p["name"], p["price"], p["stock"], cat_id)
            created_product_ids.append(pid)
            print(f"    - Creado: {p['name']} (${p['price']} COP)")
        except Exception as e:
            print(f"    [-] Error al crear {p['name']}: {e}")

    # 3. Create a seller user
    try:
        seller_res = client.register_seller("vendedor_principal", "Vendedor12345!")
        print(f"[+] Vendedor de prueba creado: 'vendedor_principal' (ID: {seller_res['id']})")
    except Exception as e:
        print(f"[*] Vendedor ya existente o error: {e}")

    # 4. Place a sample sale
    if len(created_product_ids) >= 2:
        try:
            print("[*] Registrando venta de prueba con el vendedor...")
            client.login("vendedor_principal", "Vendedor12345!")
            sale_id = client.place_sale([
                {"productId": created_product_ids[0], "quantity": 2},
                {"productId": created_product_ids[1], "quantity": 1}
            ])
            print(f"[+] Venta de prueba registrada exitosamente. ID: {sale_id}")
        except Exception as e:
            print(f"[-] Error en venta de prueba: {e}")

    print("\n[✔] Poblado de datos iniciales completado.")

def main():
    parser = argparse.ArgumentParser(description="Simple Stock Flow Seeder & CLI Tool")
    parser.add_argument("--url", default="http://localhost:8080", help="URL base del sistema")
    subparsers = parser.add_subparsers(dest="command")

    seed_parser = subparsers.add_parser("seed", help="Poblar productos y ventas de prueba vía HTTP")
    seed_parser.add_argument("--admin-user", default="admin@stockflow.local", help="Email del administrador")
    seed_parser.add_argument("--admin-password", default="AdminSecretPassword123!", help="Contraseña del administrador")

    args = parser.parse_args()
    if args.command == "seed":
        cmd_seed(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
