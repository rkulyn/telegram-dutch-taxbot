import math
from collections import OrderedDict


class TaxCalculator:

    def __init__(
            self,
            loader,
            age=False,
            year="2019",
            ruling="no",
            salary=36000,
            period="year",
            working_hours=40,
            social_security=False,
            holiday_allowance=False,
            **kwargs):

        self._tax_data = loader.load()

        self._age = age
        self._year = year
        self._period = period
        self._salary = salary
        self._ruling = ruling
        self._working_hours = working_hours
        self._social_security = social_security
        self._holiday_allowance = holiday_allowance

    @staticmethod
    def get_ruling_income(tax_data, year, ruling):
        return tax_data["rulingThreshold"][year][ruling]

    @classmethod
    def get_payroll_tax(cls, tax_data, year, salary):
        return cls.get_rates(
            brackets=tax_data["payrollTax"][year],
            salary=salary,
            rate_type="rate"
        )

    @classmethod
    def get_social_tax(cls, tax_data, year, salary, age):
        return cls.get_rates(
            brackets=tax_data["socialPercent"][year],
            salary=salary,
            rate_type="older" if age else "social"
        )

    @classmethod
    def get_general_credit(cls, tax_data, year, salary):
        return cls.get_rates(
            brackets=tax_data["generalCredit"][year],
            salary=salary,
            rate_type="rate"
        )

    @classmethod
    def get_labour_credit(cls, tax_data, year, salary):
        return cls.get_rates(
            brackets=tax_data["labourCredit"][year],
            salary=salary,
            rate_type="rate"
        )

    @staticmethod
    def get_social_credit(tax_data, year, age, social_security):
        """
          * JSON properties for socialPercent object
          * rate: Higher full rate including social contributions to be used to get proportion
          * social: Percentage of social contributions (AOW + Anw + Wlz)
          * older: Percentage for retirement age (Anw + Wlz, no contribution to AOW)

        Args:
            tax_data:
            year:
            age:
            social_security:

        Returns:

        """
        percentage = 1
        bracket = tax_data["socialPercent"][year][0]

        if not social_security:
            # Removing AOW + Anw + Wlz from total
            percentage = (bracket["rate"] - bracket["social"]) / bracket["rate"]
        elif age:
            # Removing only AOW from total
            percentage = (bracket["rate"] + bracket["older"] - bracket["social"]) / bracket["rate"]

        return percentage

    @staticmethod
    def get_rates(brackets, salary, rate_type):

        amount = 0

        for bracket in brackets:
            delta = bracket["max"] - bracket["min"] if "max" in bracket else math.inf
            tax = bracket.get(rate_type, "rate")
            is_percent_valid = -1 < tax < 1 and tax != 0

            if salary <= delta:
                amount = amount + round((salary * 100 * tax) / 100, 2) if is_percent_valid else tax
                break
            else:
                amount = amount + (delta * tax) if is_percent_valid else tax
                salary -= delta

        return amount

    def calculate(self):

        result = OrderedDict()

        salary_by_period = dict.fromkeys(("year", "month", "day", "hour"), 0)
        salary_by_period[self._period] = self._salary

        gross_year = salary_by_period['year']
        gross_year += salary_by_period["month"] * 12
        gross_year += salary_by_period["day"] * self._tax_data["workingDays"]
        gross_year += salary_by_period["hour"] * self._tax_data["workingWeeks"] * self._working_hours
        gross_year = max(gross_year, 0)

        gross_allowance = math.floor(gross_year * (0.08 / 1.08)) if self._holiday_allowance else 0

        tax_free_year = 0
        taxable_year = gross_year - gross_allowance

        if self._ruling != "no":
            ruling_income = self.get_ruling_income(
                tax_data=self._tax_data,
                year=self._year,
                ruling=self._ruling
            )

            if taxable_year > ruling_income:
                tax_free_year = taxable_year * 0.3
                taxable_year -= tax_free_year

                if taxable_year < ruling_income:
                    tax_free_year = gross_year - ruling_income
                    taxable_year = ruling_income

        taxable_year = math.floor(taxable_year)

        result["Year Gross Holiday Allowance"] = gross_allowance
        result["Year Gross Income"] = math.floor(gross_year)
        result["Month Gross Income"] = math.floor(gross_year / 12)
        result["Day Gross Income"] = math.floor(gross_year / self._tax_data["workingDays"])
        result["Hour Gross Income"] = math.floor(gross_year / (self._tax_data["workingWeeks"] * self._working_hours))
        result["Tax Free Income"] = math.floor(tax_free_year)
        result["Ruling Real Percentage"] = math.floor(tax_free_year / gross_year * 100)
        result["Taxable Income"] = taxable_year

        payroll_tax = -1 * self.get_payroll_tax(
            tax_data=self._tax_data,
            year=self._year,
            salary=taxable_year
        )

        social_tax = -1 * self.get_social_tax(
            tax_data=self._tax_data,
            year=self._year,
            salary=taxable_year,
            age=self._age

        ) if self._social_security else 0

        social_credit = self.get_social_credit(
            tax_data=self._tax_data,
            year=self._year,
            age=self._age,
            social_security=self._social_security
        )

        general_credit = social_credit * self.get_general_credit(
            tax_data=self._tax_data,
            year=self._year,
            salary=taxable_year
        )

        labour_credit = social_credit * self.get_labour_credit(
            tax_data=self._tax_data,
            year=self._year,
            salary=taxable_year
        )

        income_tax = math.floor(payroll_tax + social_tax + general_credit + labour_credit)
        income_tax = income_tax if income_tax < 0 else 0

        net_year = taxable_year + income_tax + tax_free_year

        result["Payroll Tax"] = payroll_tax
        result["Social Security Tax"] = social_tax
        result["General Tax Credit"] = general_credit
        result["Labour Tax Credit"] = labour_credit
        result["Total Income Tax"] = income_tax
        result["Year Net Holiday Allowance"] = math.floor(net_year * (0.08 / 1.08)) if self._holiday_allowance else 0
        result["Year Net Income"] = net_year
        result["Month Net Income"] = math.floor(net_year / 12)
        result["Day Net Income"] = math.floor(net_year / self._tax_data["workingDays"])
        result["Hour Net Income"] = math.floor(net_year / (self._tax_data["workingWeeks"] * self._working_hours))

        return result
