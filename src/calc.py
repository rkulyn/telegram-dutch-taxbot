import math

from collections import OrderedDict
from types import MappingProxyType

from .utils import bool2yesno


class TaxCalculator:
    """
    Tax calculator.
    Get user input data, base government tax data
    and calculate results.

    """
    __slots__ = (
        "_tax_data",
        "_age",
        "_year",
        "_period",
        "_salary",
        "_ruling",
        "_working_hours",
        "_social_security",
        "_holiday_allowance",
    )

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
        """
        Get ruling threshold from base government tax data
        by year and ruling type.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            ruling (str): Ruling type: "normal". "young", "research".

        Returns:
            (Number): Ruling threshold.

        """
        return tax_data["rulingThreshold"][year][ruling]

    @classmethod
    def get_payroll_tax(cls, tax_data, year, salary):
        """
        Get payroll tax min, max and rate from base government tax data
        and calculate tax value.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            salary (Number): Salary value.

        Returns:
            (Number): Payroll tax value.

        """
        return cls.get_rates(
            brackets=tax_data["payrollTax"][year],
            salary=salary,
            rate_type="rate"
        )

    @classmethod
    def get_social_tax(cls, tax_data, year, salary, age):
        """
        Get social tax percent from base government tax data
        and calculate tax value.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            salary (Number): Salary value.
            age (bool): True if user is older 65 years, False otherwise.

        Returns:
            (Number): Social tax value.

        """
        return cls.get_rates(
            brackets=tax_data["socialPercent"][year],
            salary=salary,
            rate_type="older" if age else "social"
        )

    @classmethod
    def get_general_credit(cls, tax_data, year, salary):
        """
        Get general credit min, max and rate from base government tax data
        and calculate credit value.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            salary (Number): Salary value.

        Returns:
            (Number): General credit value.

        """
        return cls.get_rates(
            brackets=tax_data["generalCredit"][year],
            salary=salary,
            rate_type="rate"
        )

    @classmethod
    def get_labour_credit(cls, tax_data, year, salary):
        """
        Get labour credit min, max and rate from base government tax data
        and calculate credit value.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            salary (Number): Salary value.

        Returns:
            (Number): Labour credit value.

        """
        return cls.get_rates(
            brackets=tax_data["labourCredit"][year],
            salary=salary,
            rate_type="rate"
        )

    @staticmethod
    def get_social_credit(tax_data, year, age, social_security):
        """
        Get social credit percentage from base government tax data
        and calculate credit value.

        Args:
            tax_data (dict): Government tax data.
            year (str): Calculation year.
            age (bool): True is user is older 65 years, False otherwise.
            social_security (bool): True if social security is applied, False otherwise.

        Returns:
            (Number): Social credit percentage.

        """
        percentage = 1
        bracket = tax_data["socialPercent"][year][0]

        if not social_security:
            # Removing AOW + Anw + Wlz from total
            # Percentage of social contributions (AOW + Anw + Wlz)
            percentage = (bracket["rate"] - bracket["social"]) / bracket["rate"]
        elif age:
            # Removing only AOW from total
            # Percentage for retirement age (Anw + Wlz, no contribution to AOW)
            percentage = (bracket["rate"] + bracket["older"] - bracket["social"]) / bracket["rate"]

        return percentage

    @staticmethod
    def get_rates(brackets, salary, rate_type):
        """
        Helper method to calculate rates
        for Payroll Tax, Social Tax, General Credit, Labour Credit.

        Args:
            brackets (list[dict]): Data brackets by year with min, max and rate values.
            salary (Number): Salary value.
            rate_type (str): Rate type: "rate", "older", "social".

        Returns:
            (Number): Calculated amount.

        """
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
        """
        Main calculation method.

        Returns:
            (OrderedDict): Calculation results.

        """
        result = OrderedDict()

        # Add initial data to result
        result["initial_income"] = self._salary
        result["initial_period"] = self._period.capitalize()
        result["initial_year"] = self._year
        result["initial_ha"] = bool2yesno(self._holiday_allowance)
        result["initial_ss"] = bool2yesno(self._social_security)
        result["initial_age"] = bool2yesno(self._age)
        result["initial_ruling"] = self._ruling.capitalize()
        result["initial_wh"] = self._working_hours

        # Calculation part
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

        taxable_year = math.floor(taxable_year)

        # Add calculated data to result
        result["calculated_year_gross_ha"] = gross_allowance
        result["calculated_year_gross_income"] = math.floor(gross_year)
        result["calculated_month_gross_income"] = math.floor(gross_year / 12)
        result["calculated_day_gross_income"] = math.floor(gross_year / self._tax_data["workingDays"])
        result["calculated_hour_gross_income"] = math.floor(gross_year / (self._tax_data["workingWeeks"] * self._working_hours))
        result["calculated_tax_free_income"] = math.floor(tax_free_year)
        result["calculated_ruling_percentage"] = math.floor(tax_free_year / gross_year * 100)
        result["calculated_taxable_income"] = taxable_year

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

        result["calculated_payroll_tax"] = payroll_tax
        result["calculated_ss_tax"] = social_tax
        result["calculated_general_tax_credit"] = general_credit
        result["calculated_labour_tax_credit"] = labour_credit
        result["calculated_total_income_tax"] = income_tax
        result["calculated_year_net_ha"] = math.floor(net_year * (0.08 / 1.08)) if self._holiday_allowance else 0
        result["calculated_year_net_income"] = net_year
        result["calculated_month_net_income"] = math.floor(net_year / 12)
        result["calculated_day_net_income"] = math.floor(net_year / self._tax_data["workingDays"])
        result["calculated_hour_net_income"] = math.floor(net_year / (self._tax_data["workingWeeks"] * self._working_hours))

        # Return immutable result dict
        return MappingProxyType(result)
