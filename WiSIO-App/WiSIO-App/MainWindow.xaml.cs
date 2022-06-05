using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
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

        private async void Button_NextAsync(object sender, RoutedEventArgs e)
        {
            step.Next();
            if (step.StepIndex == 4)
            {
                try
                {
                    RunPatternMatchingAlgorithm();
                    var page5 = pageList[4];
                    var page = (Page5)page5;
                    page.GenerateResults();
                }
                catch (UriFormatException)
                {
                    Growl.Error("Nie podano zdjęcia do przetworzenia!");
                }
                
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
            var process = new Process
            {
                StartInfo =
                {
                    FileName = filename,
                    Arguments = $"{Properties.Settings.Default.Image1} {Properties.Settings.Default.Image2} {Properties.Settings.Default.Arg7} {Properties.Settings.Default.Arg2} {Properties.Settings.Default.Arg3} {Properties.Settings.Default.Arg4} {Properties.Settings.Default.Arg5}",
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                },
                EnableRaisingEvents = true,
            };
            process.OutputDataReceived += OutputHandler;
            process.ErrorDataReceived += OutputHandler;
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
        }
        private void OutputHandler(object sendingProcess, DataReceivedEventArgs e)
        {
            if (e.Data != null)
                Dispatcher.BeginInvoke(System.Windows.Threading.DispatcherPriority.Send, (Action)delegate
                {
                    var page3 = pageList[3];
                    var page = (Page3)page3;
                    page.OutputBox.AppendText(e.Data);
                    page.OutputBox.AppendText(Environment.NewLine);
                    page.OutputBox.Focus();
                    page.OutputBox.CaretIndex = page.OutputBox.Text.Length;
                    page.OutputBox.ScrollToEnd();
                });
        }
    }
}
