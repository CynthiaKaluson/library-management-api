# Library Management System API

## Project Overview
A backend REST API for managing library operations including book inventory, user borrowing, and return tracking. Built as my **ALX Backend Engineering Capstone Project**.

This project demonstrates proficiency in Django, Django REST Framework, database design, authentication, and production deployment.

---

## Features

### Core Functionality
- **Book Management**: Add, view, update, and delete books (admin only)
- **User Authentication**: Register and login with token-based authentication
- **Borrow Books**: Authenticated users can borrow available books
- **Return Books**: Mark borrowed books as returned
- **Borrowing History**: Track all borrow records per user
- **Availability Tracking**: Real-time book availability updates

### Technical Features
- RESTful API architecture
- Token-based authentication (Django REST Framework tokens)
- Role-based permissions (admin vs regular users)
- Automatic due date calculation (14 days from borrow)
- Prevention of duplicate borrows
- Database relationships (One-to-Many, Foreign Keys)

---

## Tech Stack
- **Backend Framework**: Django 5.0
- **API Framework**: Django REST Framework 3.14
- **Authentication**: Token Authentication
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Server**: Gunicorn
- **Static Files**: Whitenoise
- **Deployment**: Render
- **Version Control**: Git/GitHub

---

## Database Models

### Book
- `title` (CharField): Book title
- `author` (CharField): Book author
- `isbn` (CharField): Unique 13-digit ISBN
- `published_date` (DateField): Publication date
- `copies_available` (PositiveIntegerField): Number of copies in stock
- `created_at` (DateTimeField): Auto timestamp
- `updated_at` (DateTimeField): Auto timestamp

### BorrowRecord
- `user` (ForeignKey to User): Who borrowed the book
- `book` (ForeignKey to Book): Which book was borrowed
- `borrowed_at` (DateTimeField): When book was borrowed
- `due_date` (DateField): Return deadline (auto: +14 days)
- `returned_at` (DateTimeField): When book was returned (null if not returned)
- `is_returned` (BooleanField): Return status

**Relationships:**
- One User → Many BorrowRecords
- One Book → Many BorrowRecords

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login and get token | No |

**Register Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

**Login Request:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### Books
| Method | Endpoint | Description | Auth Required | Admin Only |
|--------|----------|-------------|---------------|------------|
| GET | `/api/books/` | List all books | No | No |
| GET | `/api/books/{id}/` | Get book details | No | No |
| POST | `/api/books/` | Add new book | Yes | Yes |
| PUT | `/api/books/{id}/` | Update book | Yes | Yes |
| DELETE | `/api/books/{id}/` | Delete book | Yes | Yes |

**Create Book Request:**
```json
{
  "title": "Django for APIs",
  "author": "William S. Vincent",
  "isbn": "9781735467221",
  "published_date": "2022-01-15",
  "copies_available": 5
}
```

---

### Borrowing
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/borrow/` | List user's borrow records | Yes |
| POST | `/api/borrow/` | Borrow a book | Yes |
| POST | `/api/borrow/{id}/return_book/` | Return a book | Yes |

**Borrow Book Request:**
```json
{
  "book": 1
}
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "book": 1,
  "book_details": {
    "id": 1,
    "title": "Django for APIs",
    "author": "William S. Vincent",
    "isbn": "9781735467221",
    "copies_available": 4
  },
  "borrowed_at": "2025-01-04T14:30:00Z",
  "due_date": "2025-01-18",
  "returned_at": null,
  "is_returned": false
}
```

**Return Book Request:**
```json
POST /api/borrow/1/return_book/
```

---

## Local Setup Instructions

### Prerequisites
- Python 3.10+
- Git
- PostgreSQL (optional for local, required for production)

### 1. Clone the Repository
```bash
git clone https://github.com/CynthiaKaluson/library-management-api.git
cd library-management-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/api/books/`

---

## Testing the API

### Using Django REST Framework Browsable API
1. Open browser: `http://127.0.0.1:8000/api/books/`
2. Use the interface to view books
3. Login at top-right to test authenticated endpoints

### Using Postman/Thunder Client

**Step 1: Register**
```
POST http://127.0.0.1:8000/api/auth/register/
Body: {
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "password2": "testpass123"
}
```

**Step 2: Login**
```
POST http://127.0.0.1:8000/api/auth/login/
Body: {
  "username": "testuser",
  "password": "testpass123"
}
```
Copy the token from response.

**Step 3: Add Token to Headers**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Step 4: Borrow a Book**
```
POST http://127.0.0.1:8000/api/borrow/
Headers: Authorization: Token <your-token>
Body: {
  "book": 1
}
```

**Step 5: Return a Book**
```
POST http://127.0.0.1:8000/api/borrow/1/return_book/
Headers: Authorization: Token <your-token>
```

---

## Admin Panel

Access Django admin at: `http://127.0.0.1:8000/admin/`

Features:
- Add/edit/delete books
- View all borrow records
- Manage users

---

## Deployment

### Platform: Render

**Live URL**: `https://library-management-api-xxxx.onrender.com`

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Create Render Web Service**
   - Connect GitHub repository
   - Select branch: `main`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn library_management.wsgi`

3. **Add PostgreSQL Database**
   - Create PostgreSQL addon
   - Copy `DATABASE_URL` to environment variables

4. **Set Environment Variables**
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False
   - `DATABASE_URL`: (auto-set by Render)

5. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## Project Structure
```
library-management-api/
├── manage.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
├── library_management/
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI config for deployment
├── books/
│   ├── models.py         # Book model
│   ├── serializers.py    # Book serializer
│   ├── views.py          # Book API views
│   ├── urls.py           # Book endpoints
│   └── admin.py          # Admin configuration
├── borrowing/
│   ├── models.py         # BorrowRecord model
│   ├── serializers.py    # Borrow serializers
│   ├── views.py          # Borrow/return logic
│   ├── urls.py           # Borrowing endpoints
│   └── admin.py          # Admin configuration
└── accounts/
    ├── serializers.py    # User registration/auth
    ├── views.py          # Auth views
    └── urls.py           # Auth endpoints
```

---

## Development Timeline

This project was built incrementally over 3+ weeks:

- **Week 1**: Setup Django project, create apps, design models
- **Week 2**: Build API endpoints, add authentication, test functionality
- **Week 3**: Deploy to production, write documentation, create demo

**Commit History**: Multiple meaningful commits showing real development progress

---

## Known Issues & Future Improvements

### Current Limitations
- No pagination on book list (loads all books at once)
- No search/filter functionality
- Due dates are fixed at 14 days
- No overdue fee calculation
- No email notifications

### Planned Enhancements
- Add pagination and filtering
- Implement search by title/author/ISBN
- Add overdue notifications
- Calculate late fees
- Add book categories/genres
- Implement reservation system
- Add user profile management

---

## Security Features
- Password hashing (Django default)
- Token-based authentication
- CSRF protection
- Admin-only access for book management
- User can only see their own borrow records
- Prevention of duplicate borrows

---

## Testing

### Manual Testing Checklist
- ✅ User can register
- ✅ User can login and receive token
- ✅ Unauthenticated users can view books
- ✅ Authenticated users can borrow books
- ✅ Users cannot borrow unavailable books
- ✅ Users cannot borrow same book twice
- ✅ Users can return borrowed books
- ✅ Available copies update correctly
- ✅ Admin can add/edit/delete books
- ✅ Users can only see their own records

---

## Author

**Cynthia Okorie**  
ALX Backend Engineering Student  
Cohort [Your Cohort Number]

- **GitHub**: [@CynthiaKaluson](https://github.com/CynthiaKaluson)
- **LinkedIn**: [Your LinkedIn URL]
- **Email**: [Your Email]

---

## Acknowledgments

- **ALX Africa** for the Backend Engineering Program
- Django and Django REST Framework documentation
- Stack Overflow community for troubleshooting
- My ALX mentors and peers for guidance

---

## License

This project is for educational purposes as part of the ALX Backend Engineering Capstone Project.

---

## Demo Video

[🎥 5-Minute Demo Video Link]

In the demo, I showcase:
- User registration and authentication
- Browsing available books
- Borrowing and returning books
- Admin functionality
- API testing with Postman

---

**Project Status**: ✅ Completed and Deployed

**Last Updated**: January 2025
```

---

## 5️⃣ **LET'S COMMIT STEP BY STEP**

### **First, create `.gitignore` file:**

Create a new file called `.gitignore` in your project root:
```
*.pyc
__pycache__/
db.sqlite3
venv/
.env
staticfiles/
*.sqlite3
.DS_Store