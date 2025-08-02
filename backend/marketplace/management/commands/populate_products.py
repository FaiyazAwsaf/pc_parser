import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of products to create (default: 50)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before creating new ones'
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']

        if clear:
            self.stdout.write('Clearing existing products...')
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing products cleared.'))

        # Sample product data
        cpu_products = [
            {'name': 'Intel Core i9-13900K', 'price': 45000, 'description': 'High-performance 13th gen Intel processor with 24 cores and 32 threads. Perfect for gaming and content creation.'},
            {'name': 'AMD Ryzen 9 7900X', 'price': 42000, 'description': '12-core, 24-thread processor with excellent performance for gaming and productivity tasks.'},
            {'name': 'Intel Core i7-13700K', 'price': 35000, 'description': '16-core processor with great gaming performance and multitasking capabilities.'},
            {'name': 'AMD Ryzen 7 7700X', 'price': 28000, 'description': '8-core, 16-thread processor ideal for gaming and streaming.'},
            {'name': 'Intel Core i5-13600K', 'price': 25000, 'description': '14-core processor offering excellent value for gaming builds.'},
            {'name': 'AMD Ryzen 5 7600X', 'price': 22000, 'description': '6-core, 12-thread processor perfect for mid-range gaming systems.'},
            {'name': 'Intel Core i3-13100', 'price': 12000, 'description': 'Budget-friendly 4-core processor for basic computing needs.'},
            {'name': 'AMD Ryzen 5 5600G', 'price': 18000, 'description': 'APU with integrated graphics, great for budget builds.'},
        ]

        ram_products = [
            {'name': 'Corsair Vengeance LPX 32GB DDR4-3200', 'price': 8500, 'description': '32GB (2x16GB) DDR4 memory kit with excellent performance and reliability.'},
            {'name': 'G.Skill Trident Z RGB 16GB DDR4-3600', 'price': 6500, 'description': '16GB (2x8GB) DDR4 memory with RGB lighting and high speed.'},
            {'name': 'Kingston Fury Beast 16GB DDR4-3200', 'price': 5500, 'description': 'Reliable 16GB DDR4 memory kit for gaming and productivity.'},
            {'name': 'Corsair Dominator Platinum RGB 32GB DDR4-3600', 'price': 15000, 'description': 'Premium 32GB DDR4 memory with RGB lighting and superior performance.'},
            {'name': 'G.Skill Ripjaws V 8GB DDR4-3200', 'price': 2800, 'description': 'Budget-friendly 8GB DDR4 memory stick.'},
            {'name': 'Crucial Ballistix 16GB DDR4-3200', 'price': 5200, 'description': 'Reliable 16GB DDR4 memory for mainstream builds.'},
            {'name': 'TeamGroup T-Force Delta RGB 32GB DDR4-3600', 'price': 9500, 'description': '32GB DDR4 memory with stunning RGB effects.'},
        ]

        storage_products = [
            {'name': 'Samsung 980 PRO 1TB NVMe SSD', 'price': 12000, 'description': 'High-speed 1TB NVMe SSD with excellent performance for gaming and professional work.'},
            {'name': 'WD Black SN850X 2TB NVMe SSD', 'price': 22000, 'description': '2TB NVMe SSD optimized for gaming with fast load times.'},
            {'name': 'Crucial MX4 1TB SATA SSD', 'price': 8500, 'description': 'Reliable 1TB SATA SSD for everyday computing needs.'},
            {'name': 'Seagate Barracuda 2TB HDD', 'price': 6500, 'description': '2TB traditional hard drive for mass storage needs.'},
            {'name': 'Samsung 970 EVO Plus 500GB NVMe SSD', 'price': 6800, 'description': '500GB NVMe SSD with great performance and reliability.'},
            {'name': 'WD Blue 1TB HDD', 'price': 4200, 'description': 'Reliable 1TB hard drive for budget builds.'},
            {'name': 'Kingston NV2 1TB NVMe SSD', 'price': 7500, 'description': 'Budget-friendly 1TB NVMe SSD with decent performance.'},
            {'name': 'Crucial P3 2TB NVMe SSD', 'price': 15000, 'description': '2TB NVMe SSD offering good value for money.'},
        ]

        monitor_products = [
            {'name': 'ASUS ROG Swift PG279QM 27" 240Hz', 'price': 65000, 'description': '27-inch 1440p gaming monitor with 240Hz refresh rate and G-Sync.'},
            {'name': 'LG 27GP850-B 27" 165Hz', 'price': 32000, 'description': '27-inch 1440p IPS monitor with 165Hz refresh rate, perfect for gaming.'},
            {'name': 'Samsung Odyssey G7 32" 240Hz', 'price': 55000, 'description': '32-inch curved 1440p gaming monitor with 240Hz and HDR.'},
            {'name': 'Dell S2721DGF 27" 165Hz', 'price': 28000, 'description': '27-inch 1440p gaming monitor with excellent color accuracy.'},
            {'name': 'ASUS TUF Gaming VG24VQ 24" 144Hz', 'price': 18000, 'description': '24-inch curved 1080p gaming monitor with 144Hz refresh rate.'},
            {'name': 'AOC 24G2 24" 144Hz', 'price': 15000, 'description': 'Budget-friendly 24-inch 1080p gaming monitor with IPS panel.'},
            {'name': 'BenQ ZOWIE XL2411K 24" 144Hz', 'price': 22000, 'description': '24-inch 1080p esports monitor designed for competitive gaming.'},
        ]

        motherboard_products = [
            {'name': 'ASUS ROG Strix Z790-E Gaming WiFi', 'price': 38000, 'description': 'Premium Z790 motherboard with WiFi, RGB lighting, and excellent overclocking support.'},
            {'name': 'MSI MAG B650 Tomahawk WiFi', 'price': 18000, 'description': 'Mid-range B650 motherboard with WiFi and good feature set for AMD builds.'},
            {'name': 'Gigabyte B550 AORUS Elite V2', 'price': 12000, 'description': 'Solid B550 motherboard with good VRM and connectivity options.'},
            {'name': 'ASRock B450M PRO4', 'price': 8500, 'description': 'Budget-friendly micro-ATX motherboard for AMD Ryzen processors.'},
            {'name': 'ASUS Prime Z690-P WiFi', 'price': 16000, 'description': 'Entry-level Z690 motherboard with WiFi for Intel 12th gen processors.'},
            {'name': 'MSI B550M PRO-VDH WiFi', 'price': 9500, 'description': 'Compact micro-ATX motherboard with WiFi for budget AMD builds.'},
        ]

        psu_products = [
            {'name': 'Corsair RM850x 850W 80+ Gold', 'price': 12500, 'description': 'Fully modular 850W power supply with 80+ Gold efficiency and quiet operation.'},
            {'name': 'Seasonic Focus GX-750 750W 80+ Gold', 'price': 11000, 'description': 'High-quality 750W power supply with excellent efficiency and reliability.'},
            {'name': 'EVGA SuperNOVA 650 G5 650W 80+ Gold', 'price': 9500, 'description': 'Fully modular 650W power supply perfect for mid-range builds.'},
            {'name': 'Cooler Master MWE Gold 550W 80+ Gold', 'price': 7500, 'description': 'Reliable 550W power supply with 80+ Gold certification.'},
            {'name': 'Thermaltake Smart 500W 80+ White', 'price': 4500, 'description': 'Budget-friendly 500W power supply for basic builds.'},
            {'name': 'be quiet! Pure Power 11 600W 80+ Gold', 'price': 8500, 'description': 'Quiet and efficient 600W power supply with excellent build quality.'},
        ]

        # Combine all products with their categories
        all_products = [
            *[{**p, 'category': 'CPU'} for p in cpu_products],
            *[{**p, 'category': 'RAM'} for p in ram_products],
            *[{**p, 'category': 'Storage'} for p in storage_products],
            *[{**p, 'category': 'Monitor'} for p in monitor_products],
            *[{**p, 'category': 'Motherboard'} for p in motherboard_products],
            *[{**p, 'category': 'PSU'} for p in psu_products],
        ]

        conditions = ['Used-Like New', 'Used-Good', 'Used-Fair']

        # Get or create a default user for products
        try:
            # First try to get existing superuser
            default_user = User.objects.filter(is_superuser=True).first()
            
            if not default_user:
                # Try to get existing seller_demo user
                try:
                    default_user = User.objects.get(username='seller_demo')
                    self.stdout.write(f'Using existing demo seller user: {default_user.username}')
                except User.DoesNotExist:
                    # Create new seller_demo user
                    default_user = User.objects.create_user(
                        username='seller_demo',
                        email='seller@demo.com',
                        password='demo123',
                        first_name='Demo',
                        last_name='Seller'
                    )
                    self.stdout.write(f'Created demo seller user: {default_user.username}')
            else:
                self.stdout.write(f'Using existing superuser: {default_user.username}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error with user setup: {e}'))
            return

        created_count = 0
        for i in range(count):
            # Select a random product template
            product_template = random.choice(all_products)
            
            # Add some variation to the price (±20%)
            base_price = product_template['price']
            price_variation = random.uniform(0.8, 1.2)
            final_price = int(base_price * price_variation)
            
            # Select random condition
            condition = random.choice(conditions)
            
            # Adjust price based on condition
            if condition == 'Used-Like New':
                final_price = int(final_price * 0.95)  # 5% discount
            elif condition == 'Used-Good':
                final_price = int(final_price * 0.85)  # 15% discount
            elif condition == 'Used-Fair':
                final_price = int(final_price * 0.70)  # 30% discount

            try:
                placeholder_image = f"https://picsum.photos/200/300"

                product = Product.objects.create(
                    name=product_template['name'],
                    price=final_price,
                    category=product_template['category'],
                    condition=condition,
                    description=product_template['description'],
                    seller=default_user,
                    image=placeholder_image
                )
                created_count += 1
                
                if created_count % 10 == 0:
                    self.stdout.write(f'Created {created_count} products...')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating product: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample products!'
            )
        )
        
        # Display summary
        self.stdout.write('\n--- Product Summary ---')
        for category in ['CPU', 'RAM', 'Storage', 'Monitor', 'Motherboard', 'PSU']:
            count = Product.objects.filter(category=category).count()
            self.stdout.write(f'{category}: {count} products')
        
        self.stdout.write(f'\nTotal products in database: {Product.objects.count()}')
