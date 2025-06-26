from flask import Blueprint, session, redirect, url_for, render_template_string
from db import get_db_connection

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
def profile():
    if "user" in session:
        username = session.get("user")
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return "User not found", 404

            name = result[0]  
            
            rendered_template = render_template_string(
                f"""
                <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Profile - Traveliny</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f8; /* A lighter, softer background */
        }}
        .btn {{
            @apply font-bold py-2 px-6 rounded-lg shadow-sm hover:shadow-md transform hover:-translate-y-px transition-all duration-300;
        }}
        .btn-primary-outline {{
            @apply bg-transparent text-sky-600 border border-sky-600 hover:bg-sky-600 hover:text-white;
        }}
        .trip-card {{
            @apply bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 flex items-center space-x-6;
        }}
    </style>
</head>
<body class="min-h-screen">

    <!-- Header -->
    <header class="bg-white shadow-sm">
        <nav class="container mx-auto px-6 py-4 flex justify-between items-center">
            <h1 class="text-2xl md:text-3xl font-extrabold text-sky-800">TRAVELINY</h1>
            <div class="flex items-center space-x-4">
                <a href="#" class="text-gray-600 hover:text-sky-700">My Bookings</a>
                <img src="https://placehold.co/40x40/a3e635/4d7c0f?text=A" alt="User Avatar" class="w-10 h-10 rounded-full object-cover">
                <a href="/logout" class="text-gray-500 hover:text-red-500 transition-colors"><i class="fas fa-sign-out-alt fa-lg"></i></a>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-6 md:p-10">
        
        <!-- Profile Header -->
        <section class="bg-white rounded-2xl shadow-lg p-8 mb-10 flex flex-col md:flex-row items-center md:space-x-8">
            <div class="relative mb-6 md:mb-0">
                <img src="https://placehold.co/128x128/a3e635/4d7c0f?text=A" alt="User Avatar" class="w-32 h-32 rounded-full object-cover ring-4 ring-offset-2 ring-sky-500">
                <button class="absolute bottom-1 right-1 bg-white text-sky-600 w-8 h-8 rounded-full flex items-center justify-center shadow-md hover:bg-gray-100 transition">
                    <i class="fas fa-camera"></i>
                </button>
            </div>
            <div>
                <h2 class="text-4xl font-bold text-gray-800">{name}</h2>
                <p class="text-gray-600 mt-3 max-w-lg">Travel enthusiast exploring the world one city at a time. Lover of mountains and oceans.</p>
                <button class="btn btn-primary-outline mt-4">Edit Profile</button>
            </div>
        </section>

        <!-- Upcoming Trips -->
        <section>
            <h3 class="text-3xl font-bold text-gray-800 mb-6">Upcoming Trips</h3>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Trip Card 1 -->
                <div class="trip-card">
                    <i class="fas fa-plane-departure text-4xl text-sky-500"></i>
                    <div>
                        <h4 class="font-bold text-xl text-gray-800">Paris, France</h4>
                        <p class="text-gray-500">July 15 - July 22, 2025</p>
                        <a href="#" class="text-sky-600 hover:underline mt-2 inline-block">View Details</a>
                    </div>
                </div>

                <!-- Trip Card 2 -->
                <div class="trip-card">
                    <i class="fas fa-umbrella-beach text-4xl text-amber-500"></i>
                    <div>
                        <h4 class="font-bold text-xl text-gray-800">Bali, Indonesia</h4>
                        <p class="text-gray-500">August 5 - August 15, 2025</p>
                        <a href="#" class="text-sky-600 hover:underline mt-2 inline-block">View Details</a>
                    </div>
                </div>

                <!-- Trip Card 3 -->
                <div class="trip-card">
                     <i class="fas fa-mountain text-4xl text-green-500"></i>
                    <div>
                        <h4 class="font-bold text-xl text-gray-800">Swiss Alps</h4>
                        <p class="text-gray-500">December 20 - December 28, 2025</p>
                        <a href="#" class="text-sky-600 hover:underline mt-2 inline-block">View Details</a>
                    </div>
                </div>
                 <!-- Add New Trip Card -->
                <div class="bg-gray-50 border-2 border-dashed border-gray-300 p-6 rounded-xl shadow-inner hover:border-sky-500 transition-all duration-300 flex flex-col items-center justify-center text-center text-gray-500 hover:text-sky-600 cursor-pointer">
                    <i class="fas fa-plus text-4xl mb-2"></i>
                    <h4 class="font-bold text-xl">Plan a New Trip</h4>
                </div>
            </div>
        </section>

    </main>

</body>
</html>
""",
           name=name )
            return rendered_template

        except Exception as e:
            return "An error occurred while rendering the profile page."
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for("login.login"))
