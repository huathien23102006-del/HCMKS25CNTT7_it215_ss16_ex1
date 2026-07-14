"""
    PHẦN 1: BÁO CÁO LỖI CẤU HÌNH
    Lỗi 1: Quan hệ 1 - N (Department ↔ Student)
    Tên lỗi

    Sai thuộc tính back_populates trong quan hệ 1-N.

    Vị trí gây lỗi
    students = relationship("Student", back_populates="department_id")
    Nguyên nhân

    back_populates phải trỏ đến thuộc tính relationship ở model còn lại, không được trỏ đến cột khóa ngoại.

    Trong class Student:

    department = relationship("Department", back_populates="students")

    Tên relationship là:

    department

    nhưng lại ghi

    department_id

    Trong khi:

    department_id

    chỉ là một Column, không phải relationship.

    SQLAlchemy sẽ không thể đồng bộ hai chiều giữa:

    Department.students
    Student.department
    Cách khắc phục

    Sửa:

    students = relationship("Student", back_populates="department_id")

    thành

    students = relationship("Student", back_populates="department")
    Lỗi 2: Quan hệ 1 - 1 (Student ↔ Profile)
    Tên lỗi

    Quan hệ 1-1 chưa được cấu hình đúng, đang trở thành quan hệ 1-N.

    Vị trí gây lỗi
    profile = relationship("Profile", back_populates="student")

    và

    student_id = Column(Integer, ForeignKey("students.id"))
    Nguyên nhân

    SQLAlchemy mặc định:

    relationship(...)

    là quan hệ One-To-Many.

    Do đó:

    Một Student có thể chứa nhiều Profile.

    Ngoài ra:

    student_id

    không có:

    unique=True

    nên database cũng cho phép nhiều Profile cùng tham chiếu tới một Student.

    Điều này làm mất tính chất 1-1.

    Cách khắc phục

    Thêm

    uselist=False

    ở phía Student.

    Đồng thời thêm

    unique=True

    cho khóa ngoại.

    Sửa thành:

    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False
    )

    và

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        unique=True
    )
    Lỗi 3: Quan hệ N - N (Student ↔ Course)
    Tên lỗi

    Thiếu khai báo bảng trung gian (secondary) trong relationship.

    Vị trí gây lỗi

    Trong Student

    courses = relationship("Course", back_populates="students")

    Trong Course

    students = relationship("Student", back_populates="courses")
    Nguyên nhân

    Quan hệ nhiều-nhiều bắt buộc SQLAlchemy phải biết bảng liên kết.

    Đã khai báo:

    student_course

    nhưng lại không sử dụng.

    SQLAlchemy sẽ không biết phải JOIN thông qua bảng nào.

    Do đó sẽ báo lỗi mapping.

    Cách khắc phục

    Sửa thành

    Trong Student

    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )

    Trong Course

    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# ===========================
# Bảng trung gian Student-Course
# ===========================

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

# ===========================
# Department
# ===========================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    students = relationship(
        "Student",
        back_populates="department"
    )

# ===========================
# Student
# ===========================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    department = relationship(
        "Department",
        back_populates="students"
    )

    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False
    )

    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )

# ===========================
# Profile
# ===========================

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        unique=True
    )

    student = relationship(
        "Student",
        back_populates="profile"
    )

# ===========================
# Course
# ===========================

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )