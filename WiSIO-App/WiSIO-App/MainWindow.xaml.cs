using System.Collections.Generic;
using HandyControl.Controls;
using HandyControl.Themes;
using HandyControl.Tools;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;
using HandyControl.Tools.Extension;
using WiSIO_App.Pages;

namespace WiSIO_App
{
    public partial class MainWindow
    {
        private List<Page> pageList { get; set; }



        public MainWindow()
        {
            InitializeComponent();
            pageList = new List<Page>
            {
                new Page1(),
                new Page2(),
                new Page3(),
                new Page4(),
                new Page5(),
            };
            FrameMain.NavigationService.Navigate(pageList[step.StepIndex]);
            pageList[step.StepIndex].Show();
            
        }

        #region Change Theme
        private void ButtonConfig_OnClick(object sender, RoutedEventArgs e) => PopupConfig.IsOpen = true;

        private void ButtonSkins_OnClick(object sender, RoutedEventArgs e)
        {
            if (e.OriginalSource is Button button)
            {
                PopupConfig.IsOpen = false;
                if (button.Tag is ApplicationTheme tag)
                {
                    ((App)Application.Current).UpdateTheme(tag);
                }
                else if (button.Tag is Brush accentTag)
                {
                    ((App)Application.Current).UpdateAccent(accentTag);
                }
                else if (button.Tag is "Picker")
                {
                    var picker = SingleOpenHelper.CreateControl<ColorPicker>();
                    var window = new PopupWindow
                    {
                        PopupElement = picker,
                        WindowStartupLocation = WindowStartupLocation.CenterScreen,
                        AllowsTransparency = true,
                        WindowStyle = WindowStyle.None,
                        MinWidth = 0,
                        MinHeight = 0,
                        Title = "Select Accent Color"
                    };

                    picker.SelectedColorChanged += delegate
                    {
                        ((App)Application.Current).UpdateAccent(picker.SelectedBrush);
                        window.Close();
                    };
                    picker.Canceled += delegate { window.Close(); };
                    window.Show();
                }
            }
        }
        #endregion

        private void Button_Prev(object sender, RoutedEventArgs e)
        {
            step.Prev();
            foreach (var page in pageList)
            {
                page.Hide();
            }
            FrameMain.NavigationService.Navigate(pageList[step.StepIndex]);
            pageList[step.StepIndex].Show();
        }

        private void Button_Next(object sender, RoutedEventArgs e)
        {
            step.Next();
            foreach (var page in pageList)
            {
                page.Hide();
            }
            FrameMain.NavigationService.Navigate(pageList[step.StepIndex]);
            pageList[step.StepIndex].Show();
        }
    }
}
