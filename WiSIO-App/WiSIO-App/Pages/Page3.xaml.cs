using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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
            Properties.Settings.Default.Arg1 = DepthOfAlgorithm.Text;
            if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg1 = "3";
            }
        }

        private void FirstLayerThreshold_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            Properties.Settings.Default.Arg2 = DepthOfAlgorithm.Text;
            if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg2 = "0.02";
            }
        }

        private void ThresholdPerLayer_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            Properties.Settings.Default.Arg3 = DepthOfAlgorithm.Text;
            if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg3 = "0.06";
            }
        }

        private void ArgumentX_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            Properties.Settings.Default.Arg4 = DepthOfAlgorithm.Text;
            if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg4 = "2";
            }
        }

        private void ArgumentY_OnTextChanged(object sender, TextChangedEventArgs e)
        {
            Properties.Settings.Default.Arg5 = DepthOfAlgorithm.Text;
            if (DepthOfAlgorithm.Text == "")
            {
                Properties.Settings.Default.Arg5 = "2";
            }
        }
    }
}
