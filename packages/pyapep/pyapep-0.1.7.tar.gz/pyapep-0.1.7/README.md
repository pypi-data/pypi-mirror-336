# pyAPEP: Python Automated Enhancement Package

## Overview
pyAPEP is a library designed to assist Python developers in increasing productivity and efficiency. It provides various utilities and extended functionalities aimed at simplifying project automation and code management.

## Key Features
- **Automation Tools:** Streamline repetitive tasks with a variety of automation capabilities.
- **Extensible Modules:** Support for custom plugins and modules to enhance functionality.
- **Flexible Interface:** Intuitive API design for easy integration.

## Three Main Packages
- **isofit**
- **simide**
- **simsep**

### isofit
- `find_par(isofn, n_par, P, q, methods)`
- `best_isomodel(P, q, iso_par_nums, iso_fun_lists, iso_fun_index, tol)`
- `fit_diffT(p_list, q_list, T_list, i_ref, iso_par_nums, iso_fun_lists, iso_fun_index, tol)`
- `IAST(isotherm_list, P_i, T)`

### simide
- **Class:** `IdealColumn`

### simsep
- **Class:** `column`

## Installation
pyAPEP can be easily installed using pip:

```bash
pip install pyAPEP
