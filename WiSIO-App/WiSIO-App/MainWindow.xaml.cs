using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using HandyControl.Controls;
using HandyControl.Themes;
using HandyControl.Tools;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;
using System.Windows.Navigation;
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
                new SshConnectionPage(),
                new Page1(),
                new Page2(),
                new Page3(),
                new Page5(),
            };
            FrameMain.NavigationService.Navigate(pageList[step.StepIndex]);
            FrameMain.NavigationUIVisibility = NavigationUIVisibility.Hidden;
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
            if (step.StepIndex == 4)
            {
                RunPatternMatchingAlgorithm();
                var page5 = pageList[4];
                var page = (Page5)page5;
                page.GenerateResults();
            }
            foreach (var page in pageList)
            {
                page.Hide();
            }
            FrameMain.NavigationService.Navigate(pageList[step.StepIndex]);
            pageList[step.StepIndex].Show();
        }

        private void RunPatternMatchingAlgorithm()
        {
           
            var filename = Path.Combine(ProjectSourcePath.Value,"tresholding\\tresholding.exe");
            var proc = System.Diagnostics.Process.Start(filename,
                $"dobra_wycieta.png zla_wycieta.png 3 0.02 0.06 2 2");
            proc?.WaitForExit();
        }
    }
}
