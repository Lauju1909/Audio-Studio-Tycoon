
content = open("managers/hr.py", "r", encoding="utf-8").read()

replacements = [
    (
"""            if self.state.strike_weeks_left == 0:
                self.state.emails.insert(0, Email(
                    sender=self.state.get_text('sender_union'),
                    subject=self.state.get_text('subject_strike_ended'),
                    body=self.state.get_text('body_strike_ended'),
                    date_week=self.state.week
                ))""",
"""            if self.state.strike_weeks_left == 0:
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("strike_ended", {}))"""
    ),
    (
"""                    self.state.emails.insert(0, Email(
                        sender=self.state.get_text('sender_hr'),
                        subject=self.state.get_text('subject_training_done', name=emp.name),
                        body=self.state.get_text('body_training_done', name=emp.name, skill=emp.primary_skill, value=emp.skills[emp.primary_skill]),
                        date_week=self.state.week
                    ))""",
"""                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("training_done", {"emp": emp}))"""
    ),
    (
"""                self.state.emails.insert(0, Email(
                    sender=self.state.get_text('sender_hr'),
                    subject=self.state.get_text('subject_burnout', default='Mitarbeiter-Burnout!'),
                    body=self.state.get_text('body_burnout', name=emp.name, default=f'{emp.name} hat einen Burnout erlitten und faellt fuer {emp.sick_weeks_left} Wochen aus!'),
                    date_week=self.state.week
                ))""",
"""                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("burnout", {"emp": emp}))"""
    ),
    (
"""                    self.state.emails.insert(0, Email(
                        sender=self.state.get_text('sender_hr'),
                        subject=self.state.get_text('subject_sick_recovered', name=emp.name),
                        body=self.state.get_text('body_sick_recovered', name=emp.name),
                        date_week=self.state.week
                    ))""",
"""                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("sick_recovered", {"emp": emp}))"""
    ),
    (
"""                    self.state.emails.insert(0, Email(
                        sender=self.state.get_text('sender_hr'),
                        subject=self.state.get_text('subject_sick', name=emp.name),
                        body=self.state.get_text('body_sick', name=emp.name, weeks=emp.sick_weeks_left),
                        date_week=self.state.week
                    ))""",
"""                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("sick", {"emp": emp}))"""
    ),
    (
"""                        self.state.emails.insert(0, Email(
                            sender=self.state.get_text('sender_hr'),
                            subject=self.state.get_text('subject_burnout_quit'),
                            body=self.state.get_text('body_burnout_quit', name=emp.name),
                            date_week=self.state.week
                        ))""",
"""                        from notifications import dispatcher, Event
                        dispatcher.dispatch(Event("burnout_quit", {"emp": emp}))"""
    ),
    (
"""                    mail_subj = self.state.get_text('subject_salary_raise')
                    mail_body = self.state.get_text('body_salary_raise', name=emp.name, current=emp.salary, expected=new_salary)
                    
                    mail = Email(sender=emp.name, subject=mail_subj, body=mail_body, date_week=self.state.week)
                    mail.is_salary_request = True
                    mail.employee_idx = i
                    mail.requested_salary = new_salary
                    self.state.emails.insert(0, mail)""",
"""                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("salary_raise_request", {"emp_idx": i, "emp": emp, "new_salary": new_salary}))"""
    ),
    (
"""                self.state.emails.insert(0, Email(
                sender=e.name,
                subject=self.state.get_text('subject_quit'),
                body=self.state.get_text('body_quit', name=e.name),
                date_week=self.state.week
            ))""",
"""                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("employee_quit", {"emp": e}))"""
    ),
    (
"""                    mail = Email(
                        sender="Headhunter",
                        subject=self.state.get_text('subject_poach_offer', name=target_emp.name),
                        body=self.state.get_text('body_poach_offer', name=target_emp.name, rival=rival.name, salary=offer_salary),
                        date_week=self.state.week
                    )
                    mail.is_poach_offer = True
                    mail.employee_idx = self.state.employees.index(target_emp)
                    mail.offered_salary = offer_salary
                    self.state.emails.insert(0, mail)""",
"""                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("poach_offer", {"emp_idx": self.state.employees.index(target_emp), "emp": target_emp, "rival_name": rival.name, "offer_salary": offer_salary}))"""
    ),
    (
"""                        self.state.emails.insert(0, Email(
                            sender="System",
                            subject=self.state.get_text('subject_employee_left', name=emp.name),
                            body=self.state.get_text('body_employee_left_poach', name=emp.name),
                            date_week=self.state.week
                        ))""",
"""                        from notifications import dispatcher, Event
                        dispatcher.dispatch(Event("employee_left_poach", {"emp": emp}))"""
    )
]

for tgt, rep in replacements:
    if tgt not in content:
        print(f"Failed to find: {tgt[:40]}...")
    else:
        content = content.replace(tgt, rep)

with open("managers/hr.py", "w", encoding="utf-8") as f:
    f.write(content)
print("done hr.py")
