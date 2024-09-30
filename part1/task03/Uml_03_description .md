# HBnB Project Technical Documentation

## Introduction

This document provides a comprehensive technical overview of the HBnB project, outlining its architecture, business logic, and interactions between components. The goal is to offer a clear blueprint for the development process, using UML diagrams to represent key parts of the system.

## High-Level Architecture

### High-Level Package Diagram

The diagram below shows the three-layer architecture of the HBnB application. It includes the Presentation Layer, which handles user interactions through APIs and services, the Business Logic Layer, which contains the core models (User, Place, Review, Amenity), and the Persistence Layer, responsible for database operations. The Facade Pattern is used to simplify communication between these layers.

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
    +Controller
}
class BusinessLogicLayer {

    +User
    +Place
    +Review
    +Amenity
}
class PersistenceLayer {
    +DatabaseAccess
    +UserDao
    +PlaceDao
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```

_Explanation:_

- **Presentation Layer**: Manages the user-facing services and APIs.
- **Business Logic Layer**: Contains the application’s core entities and logic.
- **Persistence Layer**: Handles database interactions.
- **Facade Pattern**: Acts as an interface to streamline communication between layers.

## Business Logic Layer

### Class Diagram

The class diagram below illustrates the core entities of the HBnB application, focusing on the Business Logic layer. Each entity is represented as a class, with its attributes and methods. The relationships between classes, such as associations and aggregations, are also shown to highlight how these entities interact.

```mermaid
classDiagram
class User {
    +UUID4 id
    +String email
    +String name
    -String Password
    -boolean administrator
    -DateTime created_at
    -DateTime updated_at
    +create_user()
    +edit_user()
    +delete_user()
    +void login()
}

class Place {
    +UUID4 id
    -UUID4 ownerID
    +String name
    +String location
    +Float price
    +list Amenity
    +list Review
    -DateTime created_at
    -DateTime updated_at
    +create_place()
    +edit_place()
    +delete_place()
    +Float calculatePrice()
    +search()
}

class Review {
    +UUID4 id
    +Float rating
    +String comment
    -DateTime created_at
    -DateTime updated_at
    +create_review()
    +edit_review()
    +delete_review()
    +list_by_place()
}

class Amenity {
    +UUID4 id
    +String type
    -DateTime created_at
    -DateTime updated_at
    +create_amenity()
    +edit_amenity()
    +delete_amenity()
    +list()
}

User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "1" o-- "*" Amenity : contains
```

_Explanation:_

- **User**: Represents the system’s users, with attributes like email, name, and methods for login, create, edit, and delete operations.
- **Place**: Contains details of a property (e.g., location, price), and has methods for creating, editing, and calculating prices.
- **Review**: Captures user feedback for places, with attributes for rating and comment, and methods for managing reviews.
- **Amenity**: Represents features of a place, with methods to add or edit amenities.

## API Interaction Flow

### Sequence Diagrams

The following sequence diagrams show how different API calls are processed within the HBnB application. These diagrams illustrate the interaction between components in different scenarios.

#### User Registration

The user registration diagram demonstrates the flow of information from the presentation layer, through the business logic, and finally to the persistence layer when a new user is registered.

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database
User->>+API: API Call (User Registration)
API->>+BusinessLogic: Validate and Process Registration Request
BusinessLogic->>+Database: Save Data
Database-->>-BusinessLogic: Confirm Save
BusinessLogic-->>-API: Return Success/Failure
API-->>-User: Return Success/Failure
```

#### Place Creation

This diagram shows the interaction for creating a new place. It begins at the presentation layer with an API call and follows through to the business logic and database layers.

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database
User->>+API: API Call (Place Creation)
API->>+BusinessLogic: Validate and Process Creation Request
BusinessLogic->>+Database: Save Data
Database-->>-BusinessLogic: Confirm Save
BusinessLogic-->>-API: Return Success/Failure
API-->>-User: Return Success/Failure
```

#### Review Submission

The review submission process allows a user to leave feedback for a place. This diagram outlines how the system handles a new review, linking it to both the user and the place.

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database
User->>+API: API Call (Review Submission)
API->>+BusinessLogic: Validate and Process Submission Request
BusinessLogic->>+Database: Save Data
Database-->>-BusinessLogic: Confirm Save
BusinessLogic-->>-API: Return Success/Failure
API-->>-User: Return Success/Failure
```

#### Retrieve List of Places

This sequence diagram demonstrates how the system retrieves a list of places based on user queries, interacting with both the business logic and the persistence layer.

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database
User->>+API: API Call (Fetching a List of Places)
API->>+BusinessLogic: Validate and Process Retrieve Request
BusinessLogic->>+Database: Search places
Database-->>-BusinessLogic: Return a list of places
BusinessLogic-->>-API: Return Success/Failure
API-->>-User: Return a list of places
```

## Conclusion

This technical document serves as a detailed guide for the HBnB project, offering both visual representations and explanations of the system’s architecture and design. The diagrams presented here provide a strong foundation for the implementation phase, ensuring that each layer and component of the application is clearly understood.
