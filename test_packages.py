#!/usr/bin/env python3
"""
Test script to verify package loading from database
"""

import sqlite3

def test_packages():
    """Test loading packages from database"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        print("🔍 Testing package loading from database...")
        print("=" * 50)
        
        # Check if services table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='services'")
        if not cursor.fetchone():
            print("❌ Services table not found!")
            print("Please run: python setup_database.py")
            return False
        
        # Get all services organized by quantity (ascending order)
        cursor.execute('SELECT id, name, price, category, quantity, service_type, sort_order FROM services ORDER BY category, service_type, sort_order, quantity')
        services = cursor.fetchall()
        
        if not services:
            print("❌ No services found in database!")
            print("Please run: python setup_database.py")
            return False
        
        print(f"✅ Found {len(services)} packages in database")
        print()
        
        # Group by category
        categories = {}
        for service in services:
            service_id, name, price, category, quantity, service_type, sort_order = service
            if category not in categories:
                categories[category] = {}
            if service_type not in categories[category]:
                categories[category][service_type] = []
            categories[category][service_type].append({
                'id': service_id,
                'name': name,
                'price': price,
                'quantity': quantity,
                'sort_order': sort_order
            })
        
        # Display packages by category
        for category, service_types in categories.items():
            print(f"📱 {category} Services:")
            print("-" * 30)
            
            for service_type, packages in service_types.items():
                print(f"  🔹 {service_type.title()} ({len(packages)} packages):")
                # Sort packages by sort_order and quantity
                packages.sort(key=lambda x: (x['sort_order'], x['quantity']))
                for package in packages:
                    print(f"    • ID: {package['id']} | {package['name']} | Qty: {package['quantity']} | Price: ${package['price']:.2f}")
                print()
        
        # Test specific package
        print("🧪 Testing specific package data:")
        test_package = services[0]
        print(f"  Package: {test_package[1]}")
        print(f"  ID: {test_package[0]}")
        print(f"  Price: ${test_package[2]:.2f}")
        print(f"  Category: {test_package[3]}")
        print(f"  Quantity: {test_package[4]}")
        print(f"  Service Type: {test_package[5]}")
        
        conn.close()
        print("\n✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        return False

if __name__ == "__main__":
    test_packages()


