# ClaudeStack Full Workflow Example

This example demonstrates how ClaudeStack agents work together to build a complete feature from start to finish.

## Scenario: Building a Password Generator API

Let's walk through building a secure password generator API using the full ClaudeStack workflow.

## Step 1: Initial Request (Claude-Chat)

**Input to `inbox/chat.md`:**
```markdown
I need to build a secure password generator API with the following features:
- Generate passwords with customizable length (8-128 characters)
- Include/exclude character types (uppercase, lowercase, numbers, symbols)
- Multiple password generation in one request
- Rate limiting for security
- RESTful API with proper error handling
- Python Flask implementation
```

**Claude-Chat Response:**
```markdown
I understand you want to build a secure password generator API with Flask. This is a great project that involves security considerations, API design, and proper error handling.

I'm routing your request to our planning team to create a comprehensive implementation plan. The request will flow through:
1. Claude-Planner - Create technical architecture
2. Claude-Tasker - Break down into development tasks  
3. Claude-Coder - Implement the code
4. Claude-Reviewer - Review for security and quality
5. Claude-Tester - Create comprehensive tests

This ensures we build a production-ready, secure API.
```

## Step 2: Technical Planning (Claude-Planner)

**Claude-Planner Output:**
```markdown
# Password Generator API - Technical Plan

## 📌 Objective
Build a secure, RESTful password generator API using Flask with customizable options, rate limiting, and proper error handling.

## 🛠 Implementation Plan

### Architecture Decisions
- **Framework**: Flask with Flask-RESTful for clean API structure
- **Security**: Rate limiting with Flask-Limiter, input validation
- **Password Generation**: Python's `secrets` module for cryptographic randomness
- **Error Handling**: Centralized error handlers with proper HTTP status codes
- **Documentation**: OpenAPI/Swagger integration

### Key Components
1. **Password Generator Core** (`password_generator.py`)
   - Secure random generation using `secrets`
   - Character set management
   - Length validation

2. **API Endpoints** (`api.py`)
   - `POST /api/v1/generate` - Single password generation
   - `POST /api/v1/generate/batch` - Multiple password generation
   - `GET /api/v1/health` - Health check

3. **Security Layer** (`security.py`)
   - Rate limiting (100 requests/hour per IP)
   - Input validation and sanitization
   - Request logging

4. **Configuration** (`config.py`)
   - Environment-based configuration
   - Security settings
   - Rate limiting rules

### Technology Choices
- **Flask**: Lightweight, perfect for APIs
- **Flask-RESTful**: Clean resource-based API structure
- **Flask-Limiter**: Rate limiting
- **marshmallow**: Request/response validation
- **gunicorn**: Production WSGI server

### Integration Points
- Environment variables for configuration
- Logging integration
- Health check endpoint for monitoring
- CORS support for web applications

### Potential Challenges
- **Security**: Ensuring cryptographically secure randomness
- **Performance**: Efficient generation of multiple passwords
- **Validation**: Comprehensive input validation
- **Rate Limiting**: Balancing security with usability

## 🎯 Success Criteria
- API generates cryptographically secure passwords
- All endpoints return proper HTTP status codes
- Rate limiting prevents abuse
- Comprehensive error handling
- 100% test coverage on core functionality
- API documentation available

## ⚡ Next Steps
1. Break down into specific development tasks
2. Implement core password generation logic
3. Build Flask API endpoints
4. Add security and rate limiting
5. Create comprehensive tests
6. Add documentation
```

## Step 3: Task Breakdown (Claude-Tasker)

**Claude-Tasker Output:**
```markdown
# Password Generator API - Development Tasks

## 🏗️ Setup Tasks
- [ ] Create project structure and virtual environment (5 min)
- [ ] Set up requirements.txt with Flask, Flask-RESTful, Flask-Limiter (5 min)
- [ ] Create basic Flask app structure (10 min)
- [ ] Set up configuration management (15 min)

## 💻 Core Implementation Tasks
- [ ] Implement PasswordGenerator class with secure random generation (20 min)
- [ ] Add character set management (uppercase, lowercase, numbers, symbols) (15 min)
- [ ] Implement length validation (8-128 characters) (10 min)
- [ ] Create batch password generation method (15 min)

## 🌐 API Development Tasks
- [ ] Create Flask-RESTful resource for single password generation (20 min)
- [ ] Create Flask-RESTful resource for batch password generation (20 min)
- [ ] Implement health check endpoint (10 min)
- [ ] Add request/response validation with marshmallow (25 min)

## 🔒 Security Tasks
- [ ] Implement rate limiting with Flask-Limiter (15 min)
- [ ] Add input validation and sanitization (20 min)
- [ ] Create centralized error handling (15 min)
- [ ] Add request logging for security monitoring (15 min)

## 🧪 Testing Tasks
- [ ] Write unit tests for PasswordGenerator class (25 min)
- [ ] Write API endpoint tests (30 min)
- [ ] Write security and rate limiting tests (20 min)
- [ ] Write integration tests (20 min)

## 📚 Documentation Tasks
- [ ] Create API documentation with examples (20 min)
- [ ] Write README with setup and usage instructions (15 min)
- [ ] Add inline code documentation (15 min)

## 🚀 Deployment Tasks
- [ ] Create Dockerfile for containerization (15 min)
- [ ] Set up gunicorn configuration (10 min)
- [ ] Create environment variable template (10 min)

**Total Estimated Time: ~6 hours**

**Dependencies:**
- Setup tasks must be completed first
- Core implementation before API development
- Security tasks can be done in parallel with API development
- Testing should follow implementation
- Documentation can be done throughout
```

## Step 4: Code Implementation (Claude-Coder)

**Claude-Coder Output (Core Password Generator):**
```python
# password_generator.py
import secrets
import string
from typing import List, Dict, Any

class PasswordGenerator:
    """
    Secure password generator using cryptographically strong random number generation.
    """
    
    def __init__(self):
        self.character_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase, 
            'numbers': string.digits,
            'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
    
    def generate_password(self, 
                         length: int = 12,
                         include_uppercase: bool = True,
                         include_lowercase: bool = True,
                         include_numbers: bool = True,
                         include_symbols: bool = False) -> str:
        """
        Generate a single secure password.
        
        Args:
            length: Password length (8-128)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters  
            include_numbers: Include numbers
            include_symbols: Include symbols
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If invalid parameters provided
        """
        # Validate length
        if not 8 <= length <= 128:
            raise ValueError("Password length must be between 8 and 128 characters")
        
        # Build character set
        chars = self._build_character_set(
            include_uppercase, include_lowercase, 
            include_numbers, include_symbols
        )
        
        if not chars:
            raise ValueError("At least one character type must be included")
        
        # Generate password ensuring at least one character from each selected type
        password = self._generate_with_requirements(
            length, chars, include_uppercase, include_lowercase,
            include_numbers, include_symbols
        )
        
        return password
    
    def generate_multiple_passwords(self, count: int, **kwargs) -> List[str]:
        """
        Generate multiple passwords with the same parameters.
        
        Args:
            count: Number of passwords to generate (1-50)
            **kwargs: Password generation parameters
            
        Returns:
            List of generated passwords
        """
        if not 1 <= count <= 50:
            raise ValueError("Password count must be between 1 and 50")
        
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def _build_character_set(self, uppercase: bool, lowercase: bool, 
                           numbers: bool, symbols: bool) -> str:
        """Build the character set based on requirements."""
        chars = ''
        if uppercase:
            chars += self.character_sets['uppercase']
        if lowercase:
            chars += self.character_sets['lowercase']
        if numbers:
            chars += self.character_sets['numbers']
        if symbols:
            chars += self.character_sets['symbols']
        return chars
    
    def _generate_with_requirements(self, length: int, chars: str,
                                  uppercase: bool, lowercase: bool,
                                  numbers: bool, symbols: bool) -> str:
        """Generate password ensuring at least one char from each required type."""
        password = []
        
        # Ensure at least one character from each required type
        if uppercase:
            password.append(secrets.choice(self.character_sets['uppercase']))
        if lowercase:
            password.append(secrets.choice(self.character_sets['lowercase']))
        if numbers:
            password.append(secrets.choice(self.character_sets['numbers']))
        if symbols:
            password.append(secrets.choice(self.character_sets['symbols']))
        
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(secrets.choice(chars))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
```

## Step 5: Code Review (Claude-Reviewer)

**Claude-Reviewer Output:**
```markdown
# Code Review: Password Generator

## ✅ Strengths
- **Excellent Security**: Uses `secrets` module for cryptographically secure randomness
- **Input Validation**: Proper validation of length and character type requirements
- **Clear Documentation**: Well-documented methods with type hints
- **Requirement Enforcement**: Ensures at least one character from each selected type
- **Randomization**: Shuffles final password to avoid predictable patterns
- **Error Handling**: Raises appropriate ValueError exceptions

## ⚠️ Issues

### Minor Issues
1. **Symbol Set**: The symbol set could be configurable or follow a standard
   ```python
   # Consider using a more standard symbol set
   'symbols': '!@#$%^&*()-_=+[]{}\\|;:"\',.<>?/~`'
   ```

2. **Magic Numbers**: Hard-coded limits (8-128, 1-50) should be constants
   ```python
   MIN_PASSWORD_LENGTH = 8
   MAX_PASSWORD_LENGTH = 128
   MAX_BATCH_SIZE = 50
   ```

### Suggestions for Enhancement
1. **Entropy Calculation**: Add method to calculate password entropy
2. **Character Exclusion**: Allow excluding similar characters (0/O, 1/l/I)
3. **Logging**: Add security logging for audit trails

## 💡 Suggestions

### Security Enhancements
```python
def calculate_entropy(self, password: str) -> float:
    """Calculate password entropy in bits."""
    charset_size = len(set(password))
    return len(password) * math.log2(charset_size)

def generate_password_with_exclusions(self, exclude_similar: bool = False):
    """Generate password with option to exclude similar characters."""
    if exclude_similar:
        # Remove similar looking characters
        chars = chars.translate(str.maketrans('', '', '0O1lI'))
```

### Performance Optimization
```python
# For batch generation, pre-build character set once
def generate_multiple_passwords(self, count: int, **kwargs) -> List[str]:
    chars = self._build_character_set(...)  # Build once
    return [self._generate_single(chars, **kwargs) for _ in range(count)]
```

## 🎯 Verdict: **APPROVED**

The code is production-ready with excellent security practices. The minor suggestions above would enhance usability but are not blocking issues. The core security implementation is solid and follows best practices.

**Recommended Next Steps:**
1. Implement the API layer
2. Add comprehensive tests
3. Consider the enhancement suggestions for v2
```

## Step 6: Testing (Claude-Tester)

**Claude-Tester Output:**
```python
# test_password_generator.py
import pytest
import string
import re
from password_generator import PasswordGenerator

class TestPasswordGenerator:
    
    def setup_method(self):
        self.generator = PasswordGenerator()
    
    def test_default_password_generation(self):
        """Test password generation with default parameters."""
        password = self.generator.generate_password()
        
        assert len(password) == 12
        assert any(c in string.ascii_uppercase for c in password)
        assert any(c in string.ascii_lowercase for c in password)
        assert any(c in string.digits for c in password)
    
    def test_password_length_validation(self):
        """Test password length validation."""
        # Valid lengths
        for length in [8, 12, 64, 128]:
            password = self.generator.generate_password(length=length)
            assert len(password) == length
        
        # Invalid lengths
        with pytest.raises(ValueError, match="Password length must be between"):
            self.generator.generate_password(length=7)
        
        with pytest.raises(ValueError, match="Password length must be between"):
            self.generator.generate_password(length=129)
    
    def test_character_type_requirements(self):
        """Test that passwords include required character types."""
        # Test uppercase requirement
        password = self.generator.generate_password(
            length=20, include_uppercase=True, include_lowercase=False,
            include_numbers=False, include_symbols=False
        )
        assert any(c in string.ascii_uppercase for c in password)
        assert not any(c in string.ascii_lowercase for c in password)
        
        # Test symbols requirement
        password = self.generator.generate_password(
            length=20, include_symbols=True
        )
        assert any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    def test_no_character_types_selected(self):
        """Test error when no character types are selected."""
        with pytest.raises(ValueError, match="At least one character type"):
            self.generator.generate_password(
                include_uppercase=False, include_lowercase=False,
                include_numbers=False, include_symbols=False
            )
    
    def test_multiple_password_generation(self):
        """Test batch password generation."""
        passwords = self.generator.generate_multiple_passwords(
            count=5, length=10
        )
        
        assert len(passwords) == 5
        assert all(len(p) == 10 for p in passwords)
        assert len(set(passwords)) == 5  # All passwords should be unique
    
    def test_batch_size_validation(self):
        """Test batch size validation."""
        # Valid batch sizes
        passwords = self.generator.generate_multiple_passwords(count=1)
        assert len(passwords) == 1
        
        passwords = self.generator.generate_multiple_passwords(count=50)
        assert len(passwords) == 50
        
        # Invalid batch sizes
        with pytest.raises(ValueError, match="Password count must be between"):
            self.generator.generate_multiple_passwords(count=0)
        
        with pytest.raises(ValueError, match="Password count must be between"):
            self.generator.generate_multiple_passwords(count=51)
    
    def test_password_randomness(self):
        """Test that generated passwords are sufficiently random."""
        passwords = [self.generator.generate_password() for _ in range(100)]
        
        # All passwords should be unique
        assert len(set(passwords)) == 100
        
        # Test character distribution (should be roughly even)
        all_chars = ''.join(passwords)
        char_counts = {c: all_chars.count(c) for c in set(all_chars)}
        
        # No single character should dominate (> 10% of total)
        max_char_percentage = max(char_counts.values()) / len(all_chars)
        assert max_char_percentage < 0.1
    
    def test_security_requirements(self):
        """Test security-specific requirements."""
        password = self.generator.generate_password(
            length=16, include_uppercase=True, include_lowercase=True,
            include_numbers=True, include_symbols=True
        )
        
        # Should contain at least one of each required type
        assert re.search(r'[A-Z]', password)  # Uppercase
        assert re.search(r'[a-z]', password)  # Lowercase  
        assert re.search(r'[0-9]', password)  # Numbers
        assert re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)  # Symbols
    
    @pytest.mark.performance
    def test_generation_performance(self):
        """Test password generation performance."""
        import time
        
        start_time = time.time()
        passwords = self.generator.generate_multiple_passwords(
            count=1000, length=32
        )
        end_time = time.time()
        
        # Should generate 1000 passwords in under 1 second
        assert end_time - start_time < 1.0
        assert len(passwords) == 1000
```

## Summary

This example shows how ClaudeStack agents collaborate to:

1. **Understand Requirements** (Chat) - Interpret user needs
2. **Plan Architecture** (Planner) - Design technical solution
3. **Break Down Work** (Tasker) - Create actionable tasks
4. **Implement Code** (Coder) - Write production-ready code
5. **Review Quality** (Reviewer) - Ensure security and best practices
6. **Create Tests** (Tester) - Verify functionality and security

Each agent specializes in their domain while building on the previous agent's work, resulting in a comprehensive, production-ready solution.

## Key Benefits Demonstrated

- **Specialized Expertise**: Each agent focuses on their strength
- **Quality Assurance**: Multiple review stages catch issues
- **Comprehensive Coverage**: From planning to testing
- **Security Focus**: Security considerations throughout the process
- **Documentation**: Clear documentation at each stage

This workflow ensures high-quality, secure, and maintainable code that follows best practices.