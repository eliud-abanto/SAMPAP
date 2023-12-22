from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required
from models.employee import Employee
from utils.db import db
from utils.formsEmployee.forms import EmployeeForm

employees = Blueprint('employees', __name__)

@employees.route('/employees')
@login_required
def index():
    employees = Employee.query.all()
    return render_template("employees/index.html", employees=employees)

@employees.route('/list-employees', methods=["GET"])
@login_required
def items():
    items = Employee.query.all()
    return jsonify(data=[item.to_dict() for item in items])

@employees.route('/employees/create', methods=['POST'])
@login_required
def create():
    form = EmployeeForm(request.form)
    if form.validate_on_submit() and request.method == "POST":
        id = request.form['id']
        p00 = request.form['p00']
        fullname = request.form['fullname']
        birthdate = request.form['birthdate']
        management = request.form['management']
        status = request.form['status']

        # Validar p00
        emplo = Employee.query.filter_by(p00=p00).first()
        if emplo and str(emplo.id) != id:
            return jsonify(success=False, errors="Estudiante ya existe")
        
        if int(id) == 0:
            new_employee = Employee(p00,fullname,birthdate,management,status)
            db.session.add(new_employee)
            db.session.commit()
            return jsonify(success=True, msg="Estudiante agregado correctamente")
        else:
            # Para actualizar un Estudiante existente
            employee = Employee.query.get(id)
            if not employee:
                return jsonify(success=False, errors="Estudiante no encontrado")
            # Actualizar los atributos del Estudiante
            employee.p00 = p00
            employee.fullname = fullname
            employee.birthdate = birthdate
            employee.management = management
            employee.status = status

            db.session.commit()
            return jsonify(success=True, msg="Usuario actualizado correctamente")
    else:
        return jsonify(success=False, errors=form.errors)
    
@employees.route('/employee/edit/<int:employee_id>', methods=['GET'])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    return jsonify(employee.to_dict())

@employees.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify(success=True)