using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using HandyControl.Controls;

namespace WiSIO_App.Pages
{
    /// <summary>
    /// Interaction logic for Page3.xaml
    /// </summary>
    public partial class Page3 : Page
    {
        public Page3()
        {
            InitializeComponent();
        }

        private void DepthOfAlgorithm_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            var match = Regex.Match(DepthOfAlgorithm.Text, @"^[0-9]*(?:\.[0-9]+)?$", RegexOptions.IgnoreCase);
            if (match.Success)
            {
                Properties.Settings.Default.Arg1 = DepthOfAlgorithm.Text;
                Properties.Settings.Default.Save();
            }
            else if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg1 = "3";
                Properties.Settings.Default.Save();
            }
            else Growl.Warning("Wprowadzono niepoprawną wartość argumentu!");
        }

        private void FirstLayerThreshold_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            var match = Regex.Match(FirstLayerThreshold.Text, @"^(?:[1-9]\d*|0)?(?:\.\d+)?$", RegexOptions.IgnoreCase);
            if (match.Success)
            {
                Properties.Settings.Default.Arg2 = FirstLayerThreshold.Text;
                Properties.Settings.Default.Save();
            }
            else if (FirstLayerThreshold.Text == "")
            {
                Properties.Settings.Default.Arg2 = "0.02";
                Properties.Settings.Default.Save();
            }
            else Growl.Warning("Wprowadzono niepoprawną wartość argumentu!");
        }

        private void ThresholdPerLayer_OnTextChanged(object sender, TextChangedEventArgs e)
        {

            var match = Regex.Match(ThresholdPerLayer.Text, @"^(?:[1-9]\d*|0)?(?:\.\d+)?$", RegexOptions.IgnoreCase);
            if (match.Success)
            {
                Properties.Settings.Default.Arg3 = ThresholdPerLayer.Text;
                Properties.Settings.Default.Save();
            }
            else if (ThresholdPerLayer.Text == "")
            {
                Properties.Settings.Default.Arg3 = "0.06";
                Properties.Settings.Default.Save();
            }
            else Growl.Warning("Wprowadzono niepoprawną wartość argumentu!");
        }

        private void ArgumentX_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            var match = Regex.Match(ArgumentX.Text, @"^[0-9]*(?:\.[0-9]+)?$", RegexOptions.IgnoreCase);
            if (match.Success)
            {
                Properties.Settings.Default.Arg4 = ArgumentX.Text;
                Properties.Settings.Default.Save();
            }
            else if (ArgumentX.Text == "")
            {
                Properties.Settings.Default.Arg4 = "2";
                Properties.Settings.Default.Save();
            }
            else Growl.Warning("Wprowadzono niepoprawną wartość argumentu!");
        }

        private void ArgumentY_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            var match = Regex.Match(ArgumentY.Text, @"^[0-9]*(?:\.[0-9]+)?$", RegexOptions.IgnoreCase);
            if (match.Success)
            {
                Properties.Settings.Default.Arg5 = ArgumentY.Text;
                Properties.Settings.Default.Save();
            }
            else if (ArgumentY.Text == "")
            {
                Properties.Settings.Default.Arg5 = "2";
                Properties.Settings.Default.Save();
            }
            else Growl.Warning("Wprowadzono niepoprawną wartość argumentu!");
        }
    }
}
