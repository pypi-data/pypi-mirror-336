# bisslog-core-py

Business logic core (bisslog-core) - This library provides a lightweight and dependency-free implementation of
Hexagonal Architecture (Ports and Adapters) in Python. It enforces a strict
separation between domain logic, application, and infrastructure, allowing easy integration with different frameworks and external services without modifying core business logic.

It is an auxiliary library for the business layer or service domain, which allows to have a common language for operations when interacting with external components that are part of the infrastructure of the same. In other words, the business rules will not change if the architect decided to change the messaging system, it does not matter. The essential point of this library is that the domain should not change because some adapter changed.


It is to create functionalities in the backend, without dependencies and based on use cases. Minimize the cost of a possible migration to another web framework. 



## Tests

To Run test with coverage
~~~cmd
coverage run --source=bisslog -m pytest tests/
~~~


To generate report
~~~cmd
coverage html && open htmlcov/index.html
~~~