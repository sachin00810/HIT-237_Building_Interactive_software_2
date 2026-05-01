# EchoNT Object-Oriented Class Diagram

This diagram reflects the actual implementation of the EchoNT Biodiversity Monitoring system. It highlights the use of **Inheritance** (CustomUser), **Aggregation** (Observation), and **Encapsulation** (Model Methods).

```mermaid
classDiagram
    direction LR

    %% User Management App
    class CustomUser {
        <<App: users>>
        +int id
        +String username
        +String email
        +String role
        +dateTime date_joined
        +__str__() String
    }

    %% Biodiversity Data App
    class Species {
        <<App: fauna>>
        +int id
        +String common_name
        +String scientific_name
        +String taxon_group
        +String conservation_status
        +get_absolute_url() String
        +__str__() String
    }

    %% Functional Activity App
    class Observation {
        <<App: observations>>
        +int id
        +File audio_file
        +Decimal latitude
        +Decimal longitude
        +DateTime timestamp
        +Text notes
        +Boolean is_verified
        +is_recent() bool
        +__str__() String
    }

    %% Relationships (ForeignKeys)
    CustomUser "1" -- "*" Observation : researcher_records
    Species "1" -- "*" Observation : identifies_fauna

    %% Inheritance Note
    class AbstractUser {
        <<Django Core>>
    }
    AbstractUser <|-- CustomUser