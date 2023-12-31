import os
import pandas as pd
import numpy as np


# ------------------------------------- Coverts text data to excel ------------------------------------- #


def text_to_excel(text_input, text_input_2):
    raw_text_data_folder = f"{os.getcwd()}/{text_input}"
    raw_excel_data_folder = f"{os.getcwd()}/{text_input_2}"

    dir_list = os.listdir(f"{raw_text_data_folder}")
    dir_list = sorted(dir_list)

    for text in dir_list:
        # print(text)
        df = pd.read_csv(f'{raw_text_data_folder}/{text}', sep='\t')
        df.to_excel(f'{raw_excel_data_folder}/{text[:len(text) - 4]}.xlsx', 'Sheet1')


# text_to_excel('text_data', 'excel_data')

# ------------------------------------- Read excel data into a dataframe ------------------------------------- #
def read_excel_data(num, excel_input):
    raw_excel_data_folder = f"{excel_input}"
    data = pd.read_excel(
        f"{raw_excel_data_folder}/{num}.xlsx")
    data = data[["Load (N)", "Extension (mm)"]]
    return data


# ------------------------------------- A list of tests in the folder ------------------------------------- #
def test_list():
    text_input = 'text_data'
    excel_input = 'excel_data'

    if len(text_input) < 1:
        test = [0, 0, 0, 0]

    else:
        raw_text_data_folder = f"{os.getcwd()}/{text_input}"
        dir_list = os.listdir(f"{raw_text_data_folder}")
        dir_list = sorted(dir_list)
        test = []

        for text in dir_list:
            test.append(text[:len(text) - 4])

        test = sorted(test)

    return test


# ------------------------------------- Calculating the minimum & maximum ------------------------------------- #
def bound_list():
    min_extension = []
    max_extension = []

    text_input = 'text_data'
    excel_input = 'excel_data'

    if len(text_input) < 1:
        list = [0, 0, 0, 0, 0]

    else:
        for num in test_list():
            df = read_excel_data(num, excel_input)

            extension = df["Extension (mm)"]

            min_extension.append(extension.min())
            max_extension.append(extension.max())

        min_extension = sorted(min_extension)
        lower = int(min_extension[-1])

        max_extension = sorted(max_extension)
        upper = int(max_extension[0]) + 1

        list = [*range(lower, upper, 1)]

    return list


def plot_slopes(graph_name, slope_slider_lower, slope_slider_upper):
    txt = graph_name
    num1 = slope_slider_lower
    num2 = slope_slider_upper

    df = read_excel_data(graph_name, 'excel_data')
    df = df.dropna()

    extension = df["Extension (mm)"]
    extension_list = extension.values.tolist()

    force = df['Load (N)']
    force_list = force.values.tolist()

    count1 = 0
    count2 = -1
    mark_1 = []

    for i in extension_list:
        count1 = count1 + 1
        count2 = count2 + 1

        if count2 == len(extension_list) - 2:
            break
        else:
            if (extension_list[count1] < num1) and (extension_list[count2] > num1):
                mark_1.append(count1)

            elif (extension_list[count2] < num1) and (extension_list[count1] > num1):
                mark_1.append(count2)

    if len(mark_1) > 2:
        mark_1 = mark_1[1:3]
    else:
        pass

    count1 = 0
    count2 = -1
    mark_2 = []

    for i in extension_list:
        count1 = count1 + 1
        count2 = count2 + 1

        if count2 == len(extension_list) - 2:
            break
        else:
            if (extension_list[count1] < num2) and (extension_list[count2] > num2):
                mark_2.append(count2)

            elif (extension_list[count2] < num2) and (extension_list[count1] > num2):
                mark_2.append(count1)

    if len(mark_2) > 2:
        mark_2 = mark_2[1:3]
    else:
        pass

    x_1 = extension_list[mark_1[0]: mark_2[0]]
    y_1 = force_list[mark_1[0]: mark_2[0]]

    x_2 = extension_list[mark_2[1]: mark_1[1]]
    y_2 = force_list[mark_2[1]: mark_1[1]]

    x_11 = np.array(x_1)
    y_11 = np.array(y_1)

    x_22 = np.array(x_2)
    y_22 = np.array(y_2)

    try:
        m_1, b_1 = np.polyfit(x_11, y_11, 1)

        df_2 = pd.DataFrame(list(zip(x_11, m_1 * x_11 + b_1)), columns=['Extension (mm)', 'Load (N)'])

        m_2, b_2 = np.polyfit(x_22, y_22, 1)

        df_3 = pd.DataFrame(list(zip(x_11, m_1 * x_11 + b_1)), columns=['Extension (mm)', 'Load (N)'])

        return df.hvplot.line(x='Extension (mm)', y='Load (N)', title=graph_name)
        df_2.hvplot.line(x='Extension (mm)', y='Load (N)')
        df_3.hvplot.line(x='Extension (mm)', y='Load (N)')

    except:
        df_2 = pd.DataFrame(list(zip(x_1, y_1)), columns=['Extension (mm)', 'Load (N)'])
        df_3 = pd.DataFrame(list(zip(x_2, y_2)), columns=['Extension (mm)', 'Load (N)'])

        return df.hvplot.line(x='Extension (mm)', y='Load (N)', title=graph_name)
        df_2.hvplot.line(x='Extension (mm)', y='Load (N)')
        df_3.hvplot.line(x='Extension (mm)', y='Load (N)')


# plot_slopes('C1', -5, 5)


def analyze(num1, num2, hysteresis_num):
    excel_input = 'excel_data'
    raw_excel_data_folder = "excel_data"

    lower_boundary = num1
    upper_boundary = num2

    dir_list = os.listdir(f"{raw_excel_data_folder}")
    dir_list = sorted(dir_list)

    test = []
    min_extension = []
    max_extension = []
    min_force = []
    max_force = []
    slope_1 = []
    slope_2 = []
    slope_1_inter = []
    slope_2_inter = []
    stiffness = []
    stiffness_inter = []
    hysteresis = []
    hysteresis_inter = []
    area_bounded_list = []
    area_total_list = []

    test = test_list()

    def force_function(ext, mark):
        x = extension_list[mark - 3: mark + 3]
        y = force_list[mark - 3: mark + 3]

        a, b = np.polyfit(x, y, 1)

        f = a * ext + b
        return f

    def Repeat(x):
        _size = len(x)
        repeated = []
        for i in range(_size):
            k = i + 1
            for j in range(k, _size):
                if x[i] == x[j] and x[i] not in repeated:
                    repeated.append(x[i])
        return repeated

    # Finding minimums and maximums

    for num in test:
        df = read_excel_data(num, excel_input)

        extension = df["Extension (mm)"]
        force = df['Load (N)']

        min_extension.append(extension.min())
        max_extension.append(extension.max())

        min_force.append(force.min())
        max_force.append(force.max())

    # Finding the approximated slopes & stiffness

    for num in test:
        df = read_excel_data(num, excel_input)
        df = df.dropna()

        extension = df["Extension (mm)"]
        extension_list = extension.values.tolist()

        force = df['Load (N)']
        force_list = force.values.tolist()

        count1 = 0
        count2 = -1
        mark_1 = []

        for i in extension_list:
            count1 = count1 + 1
            count2 = count2 + 1

            if count2 == len(extension_list) - 2:
                break
            else:
                if (extension_list[count1] < num1) and (extension_list[count2] > num1):
                    mark_1.append(count1)

                elif (extension_list[count2] < num1) and (extension_list[count1] > num1):
                    mark_1.append(count2)

        if len(mark_1) > 2:
            mark_1 = mark_1[1:3]
        else:
            pass

        count1 = 0
        count2 = -1
        mark_2 = []

        for i in extension_list:
            count1 = count1 + 1
            count2 = count2 + 1

            if count2 == len(extension_list) - 2:
                break
            else:
                if (extension_list[count1] < num2) and (extension_list[count2] > num2):
                    mark_2.append(count2)

                elif (extension_list[count2] < num2) and (extension_list[count1] > num2):
                    mark_2.append(count1)

        if len(mark_2) > 2:
            mark_2 = mark_2[1:3]
        else:
            pass

        y_1 = force[mark_1[0]]
        y_2 = force[mark_2[0]]

        x_1 = extension[mark_1[0]]
        x_2 = extension[mark_2[0]]

        slope1 = (y_2 - y_1) / (x_2 - x_1)
        slope1 = float(slope1)
        slope_1.append(slope1)

        y_1 = force[mark_1[1]]
        y_2 = force[mark_2[1]]

        x_1 = extension[mark_1[1]]
        x_2 = extension[mark_2[1]]

        slope2 = (y_2 - y_1) / (x_2 - x_1)
        slope2 = float(slope2)
        slope_2.append(slope2)

        stiffness.append((slope1 + slope2) / 2)

        # Finding the interpolated slopes & stiffness

        x_11 = lower_boundary
        x_22 = upper_boundary

        y_11 = force_function(lower_boundary, mark_1[0])
        y_22 = force_function(upper_boundary, mark_2[0])

        slope1_inter = (y_22 - y_11) / (x_22 - x_11)
        slope1_inter = float(slope1_inter)

        x_11 = lower_boundary
        x_22 = upper_boundary

        y_11 = force_function(lower_boundary, mark_1[1])
        y_22 = force_function(upper_boundary, mark_2[1])

        slope2_inter = (y_22 - y_11) / (x_22 - x_11)
        slope2_inter = float(slope2_inter)

        x_1 = extension_list[mark_1[0]: mark_2[0]]
        y_1 = force_list[mark_1[0]: mark_2[0]]

        x_2 = extension_list[mark_2[1]: mark_1[1]]
        y_2 = force_list[mark_2[1]: mark_1[1]]

        # print(num)

        x_11 = np.array(x_1)
        y_11 = np.array(y_1)

        x_22 = np.array(x_2)
        y_22 = np.array(y_2)

        try:
            m_1, b_1 = np.polyfit(x_11, y_11, 1)

            m_2, b_2 = np.polyfit(x_22, y_22, 1)

        except:
            m_1 = slope1_inter
            m_2 = slope2_inter

        slope_1_inter.append(m_1)
        slope_2_inter.append(m_2)

        stiffness_inter.append((m_1 + m_2) / 2)

    # Finding approximated hysteresis

    for num in test:
        df = read_excel_data(num, excel_input)
        df = df.dropna()

        extension = df["Extension (mm)"]
        extension_list = extension.values.tolist()

        force = df['Load (N)']

        count1 = 0
        count2 = -1
        mark_1 = []

        for i in extension_list:
            count1 = count1 + 1
            count2 = count2 + 1

            if count2 == len(extension_list) - 2:
                break
            else:
                if (extension_list[count1] < hysteresis_num) and (extension_list[count2] > hysteresis_num):
                    mark_1.append(count1)

                elif (extension_list[count2] < hysteresis_num) and (extension_list[count1] > hysteresis_num):
                    mark_1.append(count1)

        if len(mark_1) > 2:
            mark_1 = mark_1[1:3]
        else:
            pass

        force_diff = abs(force[mark_1[0] + 2] - force[mark_1[1] + 1])

        hysteresis.append(force_diff)

        def force_function_2(ext, mark):
            x = extension.iloc[mark - 3: mark + 3]
            x = x.values.tolist()
            y = force.iloc[mark - 3: mark + 3]
            y = y.values.tolist()

            a, b = np.polyfit(x, y, 1)

            f = a * ext + b
            return f

        force_diff_inter = abs(
            force_function_2(hysteresis_num, mark_1[0]) - force_function_2(hysteresis_num, mark_1[1]))

        hysteresis_inter.append(force_diff_inter)
    '''
    # Area
    print(test)
    for num in test:
        df = raw_data(f'{num}', excel_input)
        df = df.dropna()

        extension = df["Extension (mm)"]
        extension_list = extension.values.tolist()

        force = df['Load (N)']
        force_list = force.values.tolist()

        area_low = extension.min()
        area_up = extension.max()

        count = -1
        for i in extension_list:
            count = count + 1
            if i == area_low:
                area_low_num = count
                break

        count = -1
        for i in extension_list:
            count = count + 1
            if i == area_up:
                area_up_num = count
                break

        if area_low_num > area_up_num:
            x_1 = extension_list[0:area_up_num + 1]
            y_1 = force_list[0:area_up_num + 1]

            duplicate = Repeat(x_1)
            count = 0
            while len(duplicate) > 0:
                count = count + 10
                x_1 = extension_list[count:area_up_num + 1]
                y_1 = force_list[count:area_up_num + 1]

                duplicate = Repeat(x_1)

        else:
            x_1 = extension_list[area_low_num:area_up_num + 1]
            y_1 = force_list[area_low_num:area_up_num + 1]

            duplicate = Repeat(x_1)

            count = 0

            while len(duplicate) > 0:
                count = count + 1
                x_1 = extension_list[area_low_num + count:area_up_num + 1]
                y_1 = force_list[area_low_num + count:area_up_num + 1]
                duplicate = Repeat(x_1)

        x_2 = extension_list[area_up_num:len(extension_list)]
        y_2 = force_list[area_up_num:len(extension_list)]

        f_int_1 = interpolate.interp1d(x_1, y_1, kind='quadratic')
        f_above = f_int_1(x_1)

        f_int_2 = interpolate.interp1d(x_2, y_2, kind='quadratic')

        print("f_int_2 :", f_int_2)

        f_below = f_int_2(x_2)

        area_between_total = quad(f_int_1, int(min(x_1)), int(max(x_1)))[0] - \
                             quad(f_int_2, int(min(x_1)), int(max(x_1)))[0]
        area_between_total = abs(area_between_total)
        area_total_list.append(area_between_total)

        area_between_bounded = quad(f_int_1, area_low_bound, area_up_bound)[0] - \
                               quad(f_int_2, area_low_bound, area_up_bound)[0]
        area_between_bounded = abs(area_between_bounded)
        area_bounded_list.append(area_between_bounded)
        print(num)
    '''

    new_df = pd.DataFrame(list(
        zip(test, min_extension, max_extension, min_force, max_force,slope_1_inter, slope_2_inter,
            stiffness_inter, hysteresis_inter)),
        columns=['Test', 'Minimum extension (mm)', 'Maximum extension (mm)', 'Minimum force (N)',
                 'Maximum force (N)', 'Slope above (N/mm)',
                 'Slope below (N/mm)', 'Stiffness (N/mm)',
                 f'Hysteresis at {hysteresis_num}mm (N)'])


    return new_df
