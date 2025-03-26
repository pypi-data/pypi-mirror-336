"""
Template mapper for mapping app features to templates.
"""
from typing import Dict, List, Any

class TemplateMapper:
    """
    Maps app features to templates and configurations.
    """
    
    # Expanded templates for different app types
    APP_TEMPLATES = {
        "task": {
            "base_components": ["TaskList", "TaskForm", "TaskItem", "Dashboard"],
            "data_model": {
                "Task": {
                    "id": "string",
                    "title": "string",
                    "description": "string",
                    "completed": "boolean",
                    "dueDate": "date",
                    "priority": "string",
                    "tags": "list",
                    "createdAt": "date",
                    "updatedAt": "date"
                },
                "Category": {
                    "id": "string",
                    "name": "string",
                    "color": "string"
                }
            },
            "api_endpoints": ["listTasks", "getTask", "createTask", "updateTask", "deleteTask", 
                             "listCategories", "createCategory", "updateCategory", "deleteCategory"]
        },
        "shopping": {
            "base_components": ["ProductList", "ProductDetail", "Cart", "Checkout", "OrderHistory", "CategoryList"],
            "data_model": {
                "Product": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "price": "number",
                    "image": "string",
                    "category": "string",
                    "inventory": "number",
                    "createdAt": "date",
                    "updatedAt": "date"
                },
                "Order": {
                    "id": "string",
                    "userId": "string",
                    "items": "list",
                    "totalAmount": "number",
                    "status": "string",
                    "shippingAddress": "object",
                    "paymentMethod": "string",
                    "createdAt": "date",
                    "updatedAt": "date"
                },
                "Category": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "image": "string"
                }
            },
            "api_endpoints": ["listProducts", "getProduct", "createOrder", "getOrder", "updateOrder", 
                             "listCategories", "getCategory", "listOrders", "getProductsByCategory"]
        },
        "social": {
            "base_components": ["Feed", "Post", "Comment", "Profile", "FriendList", "Notification"],
            "data_model": {
                "Post": {
                    "id": "string",
                    "userId": "string",
                    "content": "string",
                    "image": "string",
                    "createdAt": "date",
                    "likes": "number",
                    "commentCount": "number"
                },
                "Comment": {
                    "id": "string",
                    "postId": "string",
                    "userId": "string",
                    "content": "string",
                    "createdAt": "date",
                    "likes": "number"
                },
                "User": {
                    "id": "string",
                    "username": "string",
                    "bio": "string",
                    "avatar": "string",
                    "followers": "number",
                    "following": "number",
                    "createdAt": "date"
                },
                "Notification": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "content": "string",
                    "relatedId": "string",
                    "read": "boolean",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["listPosts", "getPost", "createPost", "updatePost", "deletePost", 
                             "listComments", "createComment", "deleteComment", "likePost", 
                             "followUser", "unfollowUser", "getProfile", "updateProfile"]
        },
        "fitness": {
            "base_components": ["WorkoutList", "WorkoutDetail", "ExerciseForm", "ProgressChart", "Profile"],
            "data_model": {
                "Workout": {
                    "id": "string",
                    "userId": "string",
                    "name": "string",
                    "description": "string",
                    "duration": "number",
                    "caloriesBurned": "number",
                    "date": "date",
                    "exercises": "list",
                    "createdAt": "date"
                },
                "Exercise": {
                    "id": "string",
                    "name": "string",
                    "category": "string",
                    "description": "string",
                    "sets": "number",
                    "reps": "number",
                    "weight": "number",
                    "duration": "number",
                    "notes": "string"
                },
                "Goal": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "target": "number",
                    "currentProgress": "number",
                    "startDate": "date",
                    "endDate": "date",
                    "completed": "boolean"
                }
            },
            "api_endpoints": ["listWorkouts", "getWorkout", "createWorkout", "updateWorkout", "deleteWorkout",
                             "listExercises", "createExercise", "getGoals", "updateGoal", "createGoal"]
        },
        "food": {
            "base_components": ["MenuList", "FoodItem", "Cart", "OrderForm", "ReservationForm", "RestaurantInfo"],
            "data_model": {
                "MenuItem": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "price": "number",
                    "category": "string",
                    "image": "string",
                    "ingredients": "list",
                    "allergens": "list",
                    "available": "boolean"
                },
                "Category": {
                    "id": "string",
                    "name": "string",
                    "description": "string"
                },
                "Order": {
                    "id": "string",
                    "userId": "string",
                    "items": "list",
                    "totalAmount": "number",
                    "status": "string",
                    "type": "string",
                    "deliveryAddress": "object",
                    "createdAt": "date"
                },
                "Reservation": {
                    "id": "string",
                    "userId": "string",
                    "date": "date",
                    "time": "string",
                    "partySize": "number",
                    "specialRequests": "string",
                    "status": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["listMenuItems", "getMenuItem", "createOrder", "listOrders", "updateOrder",
                             "createReservation", "updateReservation", "getAvailableTimes", "listCategories"]
        },
        "education": {
            "base_components": ["CourseList", "CourseDetail", "LessonView", "QuizForm", "StudentDashboard"],
            "data_model": {
                "Course": {
                    "id": "string",
                    "title": "string",
                    "description": "string",
                    "instructor": "string",
                    "category": "string",
                    "image": "string",
                    "duration": "number",
                    "price": "number",
                    "lessons": "list",
                    "createdAt": "date"
                },
                "Lesson": {
                    "id": "string",
                    "courseId": "string",
                    "title": "string",
                    "content": "string",
                    "videoUrl": "string",
                    "duration": "number",
                    "order": "number"
                },
                "Quiz": {
                    "id": "string",
                    "lessonId": "string",
                    "title": "string",
                    "questions": "list",
                    "passingScore": "number"
                },
                "Enrollment": {
                    "id": "string",
                    "userId": "string",
                    "courseId": "string",
                    "progress": "number",
                    "completed": "boolean",
                    "enrolledAt": "date"
                }
            },
            "api_endpoints": ["listCourses", "getCourse", "createCourse", "updateCourse", "listLessons",
                             "getLesson", "createQuiz", "submitQuizAnswer", "enrollInCourse", "trackProgress"]
        },
        "medical": {
            "base_components": ["AppointmentCalendar", "PatientList", "PatientDetail", "MedicalRecordView", "PrescriptionForm"],
            "data_model": {
                "Patient": {
                    "id": "string",
                    "name": "string",
                    "email": "string",
                    "phone": "string",
                    "dateOfBirth": "date",
                    "gender": "string",
                    "address": "object",
                    "medicalHistory": "list",
                    "createdAt": "date"
                },
                "Appointment": {
                    "id": "string",
                    "patientId": "string",
                    "doctorId": "string",
                    "date": "date",
                    "time": "string",
                    "duration": "number",
                    "type": "string",
                    "notes": "string",
                    "status": "string",
                    "createdAt": "date"
                },
                "Doctor": {
                    "id": "string",
                    "name": "string",
                    "specialization": "string",
                    "email": "string",
                    "phone": "string",
                    "availability": "object"
                },
                "MedicalRecord": {
                    "id": "string",
                    "patientId": "string",
                    "doctorId": "string",
                    "date": "date",
                    "diagnosis": "string",
                    "treatment": "string",
                    "prescription": "list",
                    "notes": "string"
                }
            },
            "api_endpoints": ["listPatients", "getPatient", "createPatient", "updatePatient",
                             "listAppointments", "createAppointment", "updateAppointment",
                             "getDoctorAvailability", "createMedicalRecord", "listMedicalRecords"]
        },
        "event": {
            "base_components": ["EventList", "EventDetail", "TicketPurchase", "Calendar", "OrganizerDashboard"],
            "data_model": {
                "Event": {
                    "id": "string",
                    "title": "string",
                    "description": "string",
                    "startDate": "date",
                    "endDate": "date",
                    "location": "object",
                    "organizer": "string",
                    "category": "string",
                    "image": "string",
                    "capacity": "number",
                    "ticketPrice": "number",
                    "status": "string",
                    "createdAt": "date"
                },
                "Ticket": {
                    "id": "string",
                    "eventId": "string",
                    "userId": "string",
                    "type": "string",
                    "price": "number",
                    "quantity": "number",
                    "purchaseDate": "date",
                    "status": "string"
                },
                "Attendee": {
                    "id": "string",
                    "ticketId": "string",
                    "name": "string",
                    "email": "string",
                    "phone": "string",
                    "checkedIn": "boolean"
                }
            },
            "api_endpoints": ["listEvents", "getEvent", "createEvent", "updateEvent", "purchaseTicket",
                             "listUserTickets", "checkInAttendee", "getEventAttendees", "cancelTicket"]
        },
        "booking": {
            "base_components": ["BookingCalendar", "ServiceList", "BookingForm", "BookingHistory", "AvailabilitySettings"],
            "data_model": {
                "Service": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "duration": "number",
                    "price": "number",
                    "category": "string",
                    "available": "boolean"
                },
                "Booking": {
                    "id": "string",
                    "userId": "string",
                    "serviceId": "string",
                    "providerId": "string",
                    "date": "date",
                    "time": "string",
                    "endTime": "string",
                    "status": "string",
                    "notes": "string",
                    "createdAt": "date"
                },
                "Provider": {
                    "id": "string",
                    "name": "string",
                    "services": "list",
                    "availability": "object",
                    "bio": "string",
                    "image": "string"
                },
                "Availability": {
                    "id": "string",
                    "providerId": "string",
                    "dayOfWeek": "number",
                    "startTime": "string",
                    "endTime": "string",
                    "breaks": "list"
                }
            },
            "api_endpoints": ["listServices", "getService", "createBooking", "updateBooking", "cancelBooking",
                             "getAvailableSlots", "listProviders", "getProviderAvailability", "listUserBookings"]
        },
        "generic": {
            "base_components": ["ListView", "DetailView", "Form", "Dashboard", "Settings"],
            "data_model": {
                "Item": {
                    "id": "string",
                    "title": "string",
                    "description": "string",
                    "status": "string",
                    "createdAt": "date",
                    "updatedAt": "date"
                },
                "Category": {
                    "id": "string",
                    "name": "string",
                    "description": "string"
                }
            },
            "api_endpoints": ["listItems", "getItem", "createItem", "updateItem", "deleteItem", 
                             "listCategories", "createCategory", "updateCategory", "deleteCategory"]
        }
    }
    
    # Feature components that can be added to any app type
    FEATURE_COMPONENTS = {
        "auth": {
            "components": ["Login", "Register", "PasswordReset", "Profile", "AccountSettings"],
            "data_model": {
                "User": {
                    "id": "string",
                    "email": "string",
                    "password": "string",
                    "name": "string",
                    "avatar": "string",
                    "createdAt": "date",
                    "lastLogin": "date"
                }
            },
            "api_endpoints": ["registerUser", "loginUser", "getCurrentUser", "updateUser", "resetPassword", "confirmEmail"]
        },
        "payment": {
            "components": ["PaymentForm", "SubscriptionList", "Invoice", "PaymentMethodManager", "PricingPlan"],
            "data_model": {
                "Payment": {
                    "id": "string",
                    "userId": "string",
                    "amount": "number",
                    "currency": "string",
                    "method": "string",
                    "status": "string",
                    "reference": "string",
                    "createdAt": "date"
                },
                "Subscription": {
                    "id": "string",
                    "userId": "string",
                    "plan": "string",
                    "status": "string",
                    "startDate": "date",
                    "endDate": "date",
                    "renewalDate": "date",
                    "paymentMethod": "string"
                },
                "PaymentMethod": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "details": "object",
                    "isDefault": "boolean",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["createPayment", "getPayment", "listSubscriptions", "createSubscription", 
                             "cancelSubscription", "addPaymentMethod", "listPaymentMethods", "generateInvoice"]
        },
        "social": {
            "components": ["SocialFeed", "LikeButton", "CommentSection", "ShareButton", "FollowButton", "ActivityStream"],
            "data_model": {
                "Like": {
                    "id": "string",
                    "userId": "string",
                    "itemId": "string",
                    "itemType": "string",
                    "createdAt": "date"
                },
                "Follow": {
                    "id": "string",
                    "followerId": "string",
                    "followingId": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["likeItem", "unlikeItem", "getLikes", "followUser", "unfollowUser", 
                             "getFollowers", "getFollowing", "shareItem"]
        },
        "messaging": {
            "components": ["ChatList", "ChatBox", "MessageItem", "NotificationBell", "ContactList", "GroupChat"],
            "data_model": {
                "Message": {
                    "id": "string",
                    "senderId": "string",
                    "receiverId": "string",
                    "content": "string",
                    "attachments": "list",
                    "createdAt": "date",
                    "read": "boolean"
                },
                "Conversation": {
                    "id": "string",
                    "participants": "list",
                    "lastMessage": "string",
                    "lastMessageAt": "date",
                    "unreadCount": "number"
                },
                "Notification": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "content": "string",
                    "read": "boolean",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["sendMessage", "getMessages", "markAsRead", "getConversations", 
                             "createConversation", "getNotifications", "markNotificationRead"]
        },
        "ai": {
            "components": ["AIChat", "RecommendationPanel", "PredictionResult", "AIAssistant", "DataAnalysis"],
            "data_model": {
                "AIRequest": {
                    "id": "string",
                    "userId": "string",
                    "prompt": "string",
                    "response": "string",
                    "model": "string",
                    "createdAt": "date"
                },
                "Recommendation": {
                    "id": "string",
                    "userId": "string",
                    "itemId": "string",
                    "itemType": "string",
                    "score": "number",
                    "reason": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["generateAIResponse", "getRecommendations", "trainModel", "getPrediction", "saveFeedback"]
        },
        "file": {
            "components": ["FileUpload", "FileList", "FileViewer", "DocumentPreview", "ImageGallery", "FolderManager"],
            "data_model": {
                "File": {
                    "id": "string",
                    "userId": "string",
                    "name": "string",
                    "type": "string",
                    "size": "number",
                    "url": "string",
                    "folderId": "string",
                    "tags": "list",
                    "createdAt": "date",
                    "updatedAt": "date"
                },
                "Folder": {
                    "id": "string",
                    "userId": "string",
                    "name": "string",
                    "parentId": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["uploadFile", "listFiles", "getFile", "deleteFile", "createFolder", "listFolders", "moveFile"]
        },
        "location": {
            "components": ["Map", "LocationSearch", "DirectionFinder", "LocationPin", "AddressForm", "NearbyItems"],
            "data_model": {
                "Location": {
                    "id": "string",
                    "userId": "string",
                    "name": "string",
                    "address": "string",
                    "coordinates": "object",
                    "type": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["saveLocation", "getLocations", "searchNearby", "getDirections", "geocodeAddress"]
        },
        "search": {
            "components": ["SearchBar", "FilterPanel", "SortOptions", "SearchResults", "AdvancedSearch", "SavedSearches"],
            "data_model": {
                "Search": {
                    "id": "string",
                    "userId": "string",
                    "query": "string",
                    "filters": "object",
                    "results": "number",
                    "savedAt": "date"
                }
            },
            "api_endpoints": ["search", "advancedSearch", "saveSearch", "getSavedSearches", "getRecentSearches"]
        },
        "analytics": {
            "components": ["Dashboard", "Chart", "StatCard", "ReportGenerator", "DataTable", "FilterSelector"],
            "data_model": {
                "Metric": {
                    "id": "string",
                    "name": "string",
                    "value": "number",
                    "period": "string",
                    "change": "number",
                    "updatedAt": "date"
                },
                "Report": {
                    "id": "string",
                    "userId": "string",
                    "name": "string",
                    "type": "string",
                    "data": "object",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["getMetrics", "generateReport", "saveReport", "getReports", "exportData"]
        },
        "calendar": {
            "components": ["Calendar", "EventForm", "DayView", "WeekView", "MonthView", "Scheduler"],
            "data_model": {
                "CalendarEvent": {
                    "id": "string",
                    "userId": "string",
                    "title": "string",
                    "description": "string",
                    "startDate": "date",
                    "endDate": "date",
                    "allDay": "boolean",
                    "recurring": "object",
                    "reminder": "object",
                    "color": "string",
                    "createdAt": "date"
                }
            },
            "api_endpoints": ["createEvent", "updateEvent", "deleteEvent", "getEvents", "getEventsByDate", "setReminder"]
        },
        "notification": {
            "components": ["NotificationList", "NotificationBadge", "PushNotificationToggle", "EmailPreferences"],
            "data_model": {
                "Notification": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "title": "string",
                    "message": "string",
                    "read": "boolean",
                    "actionLink": "string",
                    "createdAt": "date"
                },
                "NotificationSetting": {
                    "id": "string",
                    "userId": "string",
                    "type": "string",
                    "channel": "string",
                    "enabled": "boolean"
                }
            },
            "api_endpoints": ["getNotifications", "markAsRead", "markAllAsRead", "updateNotificationSettings", "sendNotification"]
        },
        "loyalty": {
            "components": ["PointsDisplay", "RewardsList", "PointsHistory", "RedeemForm", "LoyaltyTiers"],
            "data_model": {
                "LoyaltyAccount": {
                    "id": "string",
                    "userId": "string",
                    "points": "number",
                    "tier": "string",
                    "pointsToNextTier": "number",
                    "createdAt": "date"
                },
                "Transaction": {
                    "id": "string",
                    "accountId": "string",
                    "type": "string",
                    "points": "number",
                    "description": "string",
                    "createdAt": "date"
                },
                "Reward": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "pointsCost": "number",
                    "available": "boolean",
                    "expiryDate": "date"
                }
            },
            "api_endpoints": ["getPoints", "earnPoints", "redeemPoints", "getTransactions", "listRewards", "redeemReward"]
        }
    }
    
    def __init__(self):
        pass
        
    def map_features_to_templates(self, app_type: str, features: List[str]) -> Dict[str, Any]:
        """
        Map app features to templates and configurations.
        
        Args:
            app_type: The type of app (task, shopping, social, etc.)
            features: List of features to include in the app
            
        Returns:
            A dictionary containing templates, components, data models, and API endpoints
        """
        if app_type not in self.APP_TEMPLATES:
            app_type = "generic"
            
        # Start with the base template for the app type
        template_config = self.APP_TEMPLATES[app_type].copy()
        
        # Initialize components, data models, and API endpoints
        components = template_config["base_components"].copy()
        data_models = template_config["data_model"].copy()
        api_endpoints = template_config["api_endpoints"].copy()
        
        # Add components for each feature
        for feature in features:
            if feature in self.FEATURE_COMPONENTS:
                feature_config = self.FEATURE_COMPONENTS[feature]
                
                # Add components
                for component in feature_config["components"]:
                    if component not in components:
                        components.append(component)
                
                # Add data models
                for model_name, model_schema in feature_config["data_model"].items():
                    data_models[model_name] = model_schema
                    
                # Add API endpoints
                for endpoint in feature_config["api_endpoints"]:
                    if endpoint not in api_endpoints:
                        api_endpoints.append(endpoint)
        
        # Create the full template configuration
        result = {
            "app_type": app_type,
            "components": components,
            "data_models": data_models,
            "api_endpoints": api_endpoints,
            "features": features
        }
        
        return result